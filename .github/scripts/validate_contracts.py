"""
Data Contract Validator
=======================
Validates all datacontract.yml files in the repository.
Checks structure, naming conventions, schema completeness, and quality rules.
"""

import os
import sys
import yaml

# ── Config ────────────────────────────────────────────────────────────────────

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

REQUIRED_TOP_LEVEL = ["dataContractSpecification", "id", "info", "servers", "schema", "quality"]
REQUIRED_INFO = ["title", "version", "status", "description", "owner"]
REQUIRED_FIELD_ATTRS = ["name", "type", "description"]
VALID_STATUSES = ["draft", "in development", "active", "deprecated"]
VALID_FIELD_TYPES = ["string", "integer", "decimal", "float", "boolean", "date", "timestamp", "array", "object"]
VALID_QUALITY_RULES = ["not_null", "unique", "accepted_values", "min_value", "max_value", "regex", "row_count"]

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def check(errors, condition, message):
    if not condition:
        errors.append(f"  ❌ {message}")
    return condition

# ── Validators ────────────────────────────────────────────────────────────────

def validate_top_level(contract, errors):
    for field in REQUIRED_TOP_LEVEL:
        check(errors, field in contract, f"Chybí povinné pole: `{field}`")

def validate_info(contract, errors):
    info = contract.get("info", {})
    if not isinstance(info, dict):
        errors.append("  ❌ Sekce `info` musí být objekt")
        return
    for field in REQUIRED_INFO:
        check(errors, field in info, f"Chybí `info.{field}`")

    # Naming convention: title must start with DP_
    title = info.get("title", "")
    check(errors, title.startswith("DP_"), f"`info.title` musí začínat prefixem DP_ (aktuálně: '{title}')")

    # Status must be valid
    status = info.get("status", "")
    check(errors, status in VALID_STATUSES, f"`info.status` musí být jeden z {VALID_STATUSES} (aktuálně: '{status}')")

    # Version semver check
    version = str(info.get("version", ""))
    parts = version.split(".")
    check(errors, len(parts) == 3 and all(p.isdigit() for p in parts),
          f"`info.version` musí být ve formátu major.minor.patch (aktuálně: '{version}')")

def validate_servers(contract, errors):
    servers = contract.get("servers", {})
    if not isinstance(servers, dict) or len(servers) == 0:
        errors.append("  ❌ Sekce `servers` musí obsahovat alespoň jeden server")
        return
    for server_name, server in servers.items():
        if not isinstance(server, dict):
            errors.append(f"  ❌ Server `{server_name}` musí být objekt")
            continue
        for field in ["type", "catalog", "schema", "table"]:
            check(errors, field in server, f"Server `{server_name}` chybí pole `{field}`")

def validate_schema(contract, errors):
    schema = contract.get("schema", [])
    if not isinstance(schema, list) or len(schema) == 0:
        errors.append("  ❌ Sekce `schema` musí obsahovat alespoň jednu tabulku")
        return

    all_field_names = set()

    for table in schema:
        if not isinstance(table, dict):
            errors.append("  ❌ Každá tabulka v `schema` musí být objekt")
            continue

        table_name = table.get("name", "<bez názvu>")
        check(errors, "name" in table, "Tabulka v `schema` nemá `name`")
        check(errors, "fields" in table, f"Tabulka `{table_name}` nemá `fields`")

        fields = table.get("fields", [])
        if not isinstance(fields, list) or len(fields) == 0:
            errors.append(f"  ❌ Tabulka `{table_name}` musí mít alespoň jedno pole")
            continue

        for field in fields:
            if not isinstance(field, dict):
                errors.append(f"  ❌ Pole v tabulce `{table_name}` musí být objekt")
                continue
            for attr in REQUIRED_FIELD_ATTRS:
                check(errors, attr in field, f"Pole `{field.get('name', '?')}` v tabulce `{table_name}` chybí `{attr}`")

            field_type = field.get("type", "")
            check(errors, field_type in VALID_FIELD_TYPES,
                  f"Pole `{field.get('name', '?')}` má neplatný typ `{field_type}` (povolené: {VALID_FIELD_TYPES})")

            all_field_names.add(field.get("name", ""))

    return all_field_names

def validate_quality(contract, errors, valid_field_names):
    quality = contract.get("quality", [])
    if not isinstance(quality, list) or len(quality) == 0:
        errors.append("  ❌ Sekce `quality` musí obsahovat alespoň jedno pravidlo")
        return

    for rule in quality:
        if not isinstance(rule, dict):
            errors.append("  ❌ Každé quality pravidlo musí být objekt")
            continue
        check(errors, "rule" in rule, "Quality pravidlo chybí `rule`")
        check(errors, "field" in rule, "Quality pravidlo chybí `field`")
        check(errors, "description" in rule, "Quality pravidlo chybí `description`")

        rule_type = rule.get("rule", "")
        check(errors, rule_type in VALID_QUALITY_RULES,
              f"Neplatný typ quality pravidla `{rule_type}` (povolené: {VALID_QUALITY_RULES})")

        field_ref = rule.get("field", "")
        if valid_field_names:
            check(errors, field_ref in valid_field_names,
                  f"Quality pravidlo odkazuje na neexistující pole `{field_ref}`")

def validate_contract(path):
    errors = []
    try:
        contract = load_yaml(path)
        if contract is None:
            return [f"  ❌ Soubor je prázdný nebo nevalidní YAML"]
    except yaml.YAMLError as e:
        return [f"  ❌ YAML syntax error: {e}"]
    except Exception as e:
        return [f"  ❌ Nelze načíst soubor: {e}"]

    validate_top_level(contract, errors)
    validate_info(contract, errors)
    validate_servers(contract, errors)
    field_names = validate_schema(contract, errors)
    validate_quality(contract, errors, field_names or set())

    return errors

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    report_lines = []
    total_files = 0
    total_errors = 0
    failed_teams = []

    print("\n" + "=" * 60)
    print("  DATA CONTRACT VALIDATOR")
    print("=" * 60)

    for team_folder in TEAM_FOLDERS:
        contract_path = os.path.join(repo_root, team_folder, "datacontract.yml")

        if not os.path.exists(contract_path):
            msg = f"\n⚠️  [{team_folder}] datacontract.yml nenalezen – přeskakuji"
            print(msg)
            report_lines.append(msg)
            continue

        total_files += 1
        errors = validate_contract(contract_path)

        if errors:
            total_errors += len(errors)
            failed_teams.append(team_folder)
            header = f"\n❌ [{team_folder}] FAILED ({len(errors)} chyb)"
            print(header)
            report_lines.append(header)
            for e in errors:
                print(e)
                report_lines.append(e)
        else:
            ok = f"\n✅ [{team_folder}] OK"
            print(ok)
            report_lines.append(ok)

    # Summary
    summary = f"""
{"=" * 60}
VÝSLEDEK VALIDACE
{"=" * 60}
Celkem souborů:  {total_files}
Bez chyb:        {total_files - len(failed_teams)}
S chybami:       {len(failed_teams)}
Celkem chyb:     {total_errors}
{"=" * 60}
"""
    print(summary)
    report_lines.append(summary)

    # Write report file
    report_path = os.path.join(repo_root, "validation_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    if failed_teams:
        print(f"❌ Validace SELHALA pro: {', '.join(failed_teams)}")
        sys.exit(1)
    else:
        print("✅ Všechny data contracty jsou validní!")
        sys.exit(0)

if __name__ == "__main__":
    main()
