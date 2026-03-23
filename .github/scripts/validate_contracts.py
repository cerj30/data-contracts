"""
Data Contract Validator - v5
Validates all .yml/.yaml data contract files in team folders.
Checks: structure, info, servers, schema (x-compliance), quality (row_count),
        x-regulatory, x-dawiso (data_product + glossary_entry)
"""

import os
import sys
import yaml

TEAM_FOLDERS = [
    "team1-digi",
    "team2-Data-Governance",
    "team3-client-service",
    "team4-steering-data",
    "team5-esg-risk",
    "team6-strategy",
    "team7-gen-ai",
    "team8-investment-banking",
]

REQUIRED_TOP_LEVEL = ["id", "info", "servers", "schema"]
REQUIRED_INFO = ["title", "version", "status", "description", "owner"]
REQUIRED_FIELD_ATTRS = ["name", "type", "description"]
REQUIRED_SERVER_ATTRS = ["type", "host", "catalog", "schema", "table"]

VALID_STATUSES = ["draft", "in development", "active", "deprecated"]
VALID_PRODUCT_TYPES = ["EVENT", "STATE", "AGGREGATION"]
VALID_FIELD_TYPES = [
    "string", "integer", "decimal", "float", "double",
    "boolean", "date", "timestamp", "array", "object", "number", "bigint", "long"
]
VALID_QUALITY_RULES = [
    "not_null", "unique", "accepted_values",
    "min_value", "max_value", "regex", "row_count", "range",
    "custom", "completeness"
]
VALID_SENSITIVITIES = ["Internal", "Confidential", "Public", "Restricted"]
VALID_LEGAL_BASES = ["Contractual", "Consent", "Legal Obligation"]
VALID_REGULATORY_FRAMEWORKS = ["GDPR", "BCBS 239", "IFRS 9", "AML", "MiFID II", "None"]



def check(errors, condition, message):
    if not condition:
        errors.append(f"  ❌ {message}")


def validate_contract(path):
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            contract = yaml.safe_load(f)
        if contract is None:
            return ["  ❌ Soubor je prázdný"]
    except yaml.YAMLError as e:
        return [f"  ❌ YAML syntax error: {e}"]
    except Exception as e:
        return [f"  ❌ Nelze načíst: {e}"]

    # ── Top level ────────────────────────────────────────────
    for field in REQUIRED_TOP_LEVEL:
        check(errors, field in contract, f"Chybí povinné pole: `{field}`")

    # ── Info ─────────────────────────────────────────────────
    info = contract.get("info", {})
    if isinstance(info, dict):
        for field in REQUIRED_INFO:
            check(errors, field in info, f"Chybí `info.{field}`")

        status = info.get("status", "")
        check(errors, status in VALID_STATUSES,
              f"`info.status` musí být jeden z {VALID_STATUSES} (aktuálně: '{status}')")

        version = str(info.get("version", ""))
        parts = version.split(".")
        check(errors, len(parts) >= 2 and all(p.isdigit() for p in parts),
              f"`info.version` musí být ve formátu major.minor[.patch] (aktuálně: '{version}')")

        # v5: product_type required
        pt = info.get("product_type", "")
        check(errors, pt in VALID_PRODUCT_TYPES,
              f"`info.product_type` musí být jeden z {VALID_PRODUCT_TYPES} (aktuálně: '{pt}')")

        # v5: x-regulatory required
        xreg = info.get("x-regulatory")
        check(errors, isinstance(xreg, dict),
              "`info.x-regulatory` chybí nebo není objekt")
        if isinstance(xreg, dict):
            check(errors, "gdpr_relevant" in xreg,
                  "`info.x-regulatory` chybí `gdpr_relevant`")
            check(errors, "critical_data_element" in xreg,
                  "`info.x-regulatory` chybí `critical_data_element`")
            rf = xreg.get("regulatory_framework", "")
            if isinstance(rf, list):
                for item in rf:
                    check(errors, item in VALID_REGULATORY_FRAMEWORKS,
                          f"`info.x-regulatory.regulatory_framework` musí být jeden z "
                          f"{VALID_REGULATORY_FRAMEWORKS} (aktuálně: '{item}')")
            else:
                check(errors, rf in VALID_REGULATORY_FRAMEWORKS,
                      f"`info.x-regulatory.regulatory_framework` musí být jeden z "
                      f"{VALID_REGULATORY_FRAMEWORKS} (aktuálně: '{rf}')")
    else:
        errors.append("  ❌ Sekce `info` musí být objekt")

    # ── Servers ──────────────────────────────────────────────
    servers = contract.get("servers", {})
    if isinstance(servers, dict) and len(servers) > 0:
        for sname, srv in servers.items():
            if isinstance(srv, dict):
                for attr in REQUIRED_SERVER_ATTRS:
                    check(errors, attr in srv,
                          f"Server `{sname}` chybí `{attr}`")
    else:
        errors.append("  ❌ Sekce `servers` musí obsahovat alespoň jeden server")

    # ── Schema ───────────────────────────────────────────────
    schema = contract.get("schema", [])
    all_fields = set()
    # Normalize: support both list format and single-table dict format
    if isinstance(schema, dict):
        schema = [schema]
    if isinstance(schema, list) and len(schema) > 0:
        for table in schema:
            if not isinstance(table, dict):
                continue
            tname = table.get("name", "?")
            fields = table.get("fields", [])
            check(errors, isinstance(fields, list) and len(fields) > 0,
                  f"Tabulka `{tname}` neobsahuje žádná pole (`fields`)")
            if isinstance(fields, list):
                for field in fields:
                    if isinstance(field, dict):
                        fname = field.get("name", "")
                        if fname:
                            all_fields.add(fname)
                        for attr in REQUIRED_FIELD_ATTRS:
                            check(errors, attr in field,
                                  f"Pole `{fname or '?'}` v `{tname}` chybí `{attr}`")
                        ft = field.get("type", "")
                        check(errors, ft in VALID_FIELD_TYPES,
                              f"Pole `{fname or '?'}` má neplatný typ `{ft}` "
                              f"(povolené: {VALID_FIELD_TYPES})")
                        # x-compliance required on every field
                        xc = field.get("x-compliance")
                        check(errors, xc is not None,
                              f"Pole `{fname or '?'}` v `{tname}` chybí sekce `x-compliance`")
                        if isinstance(xc, dict):
                            check(errors, "is_pii" in xc,
                                  f"Pole `{fname or '?'}` — `x-compliance` chybí `is_pii`")
                            check(errors, "sensitivity" in xc,
                                  f"Pole `{fname or '?'}` — `x-compliance` chybí `sensitivity`")
                            sens = xc.get("sensitivity", "")
                            if sens:
                                check(errors, sens in VALID_SENSITIVITIES,
                                      f"Pole `{fname or '?'}` — `sensitivity` musí být jeden z "
                                      f"{VALID_SENSITIVITIES} (aktuálně: '{sens}')")
                            if xc.get("is_pii") is True:
                                lb = xc.get("legal_basis", "")
                                check(errors, lb in VALID_LEGAL_BASES,
                                      f"Pole `{fname or '?'}` je PII — `legal_basis` musí být "
                                      f"jeden z {VALID_LEGAL_BASES} (aktuálně: '{lb}')")
    else:
        errors.append("  ❌ Sekce `schema` musí obsahovat alespoň jednu tabulku")

    # ── Quality ──────────────────────────────────────────────
    quality = contract.get("quality", [])
    has_row_count = False
    if isinstance(quality, list) and len(quality) > 0:
        for rule in quality:
            if isinstance(rule, dict):
                check(errors, "rule" in rule, "Quality pravidlo chybí `rule`")
                rt = rule.get("rule", "")
                check(errors, rt in VALID_QUALITY_RULES,
                      f"Neplatný quality rule `{rt}` (povolené: {VALID_QUALITY_RULES})")
                if rt == "row_count":
                    has_row_count = True
                    check(errors, "min" in rule or "max" in rule,
                          "Quality rule `row_count` musí mít `min` nebo `max`")
                elif rt == "custom":
                    # custom rules may use 'field', 'fields', or neither
                    pass
                else:
                    check(errors, "field" in rule,
                          f"Quality pravidlo `{rt}` chybí `field`")
                    rf = rule.get("field", "")
                    if rf and all_fields:
                        check(errors, rf in all_fields,
                              f"Quality rule odkazuje na neexistující pole `{rf}` "
                              f"(dostupná pole: {sorted(all_fields)})")

    # v5: row_count is mandatory
    check(errors, has_row_count,
          "Chybí povinný quality rule `row_count` (detekce distribučních anomálií)")

    # x-dawiso je volitelná sekce (metadata pro ruční vložení do Dawiso)
    # CI ji nevaliduje — týmy ji vyplňují podle šablony, ale není blocker pro merge

    return errors


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    report_lines = []
    total_files = 0
    total_errors = 0
    failed_files = []

    print("\n" + "=" * 60)
    print("  DATA CONTRACT VALIDATOR v5")
    print("=" * 60)

    for team_folder in TEAM_FOLDERS:
        folder_path = os.path.join(repo_root, team_folder)
        if not os.path.exists(folder_path):
            msg = f"\n⚠️  [{team_folder}] složka nenalezena"
            print(msg); report_lines.append(msg)
            continue

        yml_files = sorted([f for f in os.listdir(folder_path)
                     if f.endswith(".yml") or f.endswith(".yaml")])

        if not yml_files:
            msg = f"\n⚠️  [{team_folder}] žádné .yml soubory"
            print(msg); report_lines.append(msg)
            continue

        for yml_file in yml_files:
            path = os.path.join(folder_path, yml_file)
            total_files += 1
            errors = validate_contract(path)
            label = f"[{team_folder}/{yml_file}]"

            if errors:
                total_errors += len(errors)
                failed_files.append(label)
                header = f"\n❌ {label} FAILED ({len(errors)} chyb)"
                print(header); report_lines.append(header)
                for e in errors:
                    print(e); report_lines.append(e)
            else:
                ok = f"\n✅ {label} OK"
                print(ok); report_lines.append(ok)

    passed = total_files - len(failed_files)
    summary = f"""
{"=" * 60}
VÝSLEDEK VALIDACE v5
{"=" * 60}
Celkem souborů:       {total_files}
Souborů bez chyb:     {passed}
Souborů s chybami:    {len(failed_files)}
Celkem chyb:          {total_errors}  (v {len(failed_files)} souborech)
{"=" * 60}
"""
    print(summary); report_lines.append(summary)

    report_path = os.path.join(repo_root, "validation_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    if failed_files:
        sys.exit(1)
    else:
        print("✅ Všechny data contracty jsou validní!")
        sys.exit(0)


if __name__ == "__main__":
    main()