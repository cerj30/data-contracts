"""
validate_contracts.py — Nova Banka Data Mesh
Validates all Data Contract YAML files against prompt v3.3 requirements.
Checks: core structure, x-compliance (incl. regulatory_basis), extended GDPR,
        regulatory_mapping (10 regulations), AI Act / FRIA, and FIBO glossary entry.
"""

import os
import sys
import yaml
import glob

# ── Configuration ────────────────────────────────────────────────────────────

CONTRACT_GLOBS = ["**/*.yml", "**/*.yaml"]
REPORT_PATH   = "validation_report.txt"

# 10 mandatory regulations from prompt v3.3
REQUIRED_REGULATIONS = [
    "BCBS 239", "BASEL IV", "EBA", "DORA",
    "AML", "MiFID II", "PSD2", "GDPR", "AI Act", "IFRS 9"
]

VALID_STATUSES = {"Contributes", "Restricts", "Both", "N/A"}

VALID_LEGAL_BASES = {
    "Contractual", "Consent", "Legal Obligation", "Legitimate Interest"
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def err(path, msg):
    return f"  ❌  [{path}] {msg}"

def warn(path, msg):
    return f"  ⚠️   [{path}] {msg}"

def ok(msg):
    return f"  ✅  {msg}"

# ── Validation rules ──────────────────────────────────────────────────────────

def check_core(path, doc, issues):
    """Check top-level mandatory fields."""
    info = doc.get("info", {})
    for field in ["title", "name", "product_type", "version", "status", "description"]:
        if not info.get(field):
            issues.append(err(path, f"info.{field} is missing or empty"))

    if not doc.get("servers"):
        issues.append(err(path, "servers block is missing"))
    if not doc.get("schema"):
        issues.append(err(path, "schema block is missing"))
    if not doc.get("quality"):
        issues.append(err(path, "quality block is missing"))
    if not doc.get("sla"):
        issues.append(err(path, "sla block is missing"))


def check_extended_gdpr(path, doc, issues):
    """v3.3 — Check extended GDPR fields in x-regulatory."""
    reg = doc.get("info", {}).get("x-regulatory", {})
    if not reg:
        issues.append(err(path, "info.x-regulatory block is missing"))
        return
    for field in ["gdpr_relevant", "critical_data_element", "regulatory_framework",
                  "data_minimization", "right_to_erasure", "purpose_limitation"]:
        if field not in reg:
            issues.append(err(path, f"info.x-regulatory.{field} is missing (v3.3 requirement)"))


def check_fields_compliance(path, doc, issues):
    """Check every schema field has x-compliance with regulatory_basis (v3.3)."""
    schema = doc.get("schema", [])
    # Normalise: single-table dict → list
    schemas = [schema] if isinstance(schema, dict) else schema
    for table in schemas:
        for field in table.get("fields", []):
            fname = field.get("name", "<unnamed>")
            xc = field.get("x-compliance")
            if not xc:
                issues.append(err(path, f"field '{fname}' is missing x-compliance block"))
                continue

            # is_pii + sensitivity always required
            if "is_pii" not in xc:
                issues.append(err(path, f"field '{fname}' x-compliance.is_pii is missing"))
            if "sensitivity" not in xc:
                issues.append(err(path, f"field '{fname}' x-compliance.sensitivity is missing"))

            # legal_basis required only when is_pii is true
            if xc.get("is_pii") is True:
                lb = xc.get("legal_basis")
                if not lb:
                    issues.append(err(path, f"field '{fname}' is PII but legal_basis is missing"))
                elif lb not in VALID_LEGAL_BASES:
                    issues.append(err(path, f"field '{fname}' legal_basis '{lb}' is not valid "
                                           f"(must be one of: {', '.join(VALID_LEGAL_BASES)})"))

            # v3.3 — regulatory_basis required on every field
            if not xc.get("regulatory_basis"):
                issues.append(err(path, f"field '{fname}' x-compliance.regulatory_basis is missing (v3.3)"))


def check_quality(path, doc, issues):
    """Check quality rules — must include not_null, unique, row_count."""
    # Rules that operate on the whole table — field attribute is NOT required
    TABLE_LEVEL_RULES = {
        "row_count", "schema_validity", "custom", "completeness"
    }
    # All recognised rule types
    VALID_RULES = {
        "not_null", "unique", "accepted_values", "min_value", "max_value",
        "regex", "row_count", "range", "custom", "completeness", "schema_validity"
    }

    quality = doc.get("quality", [])
    rules = {r.get("rule") for r in quality}

    # These three must always be present
    for required_rule in ["not_null", "unique", "row_count"]:
        if required_rule not in rules:
            issues.append(err(path, f"quality rule '{required_rule}' is missing"))

    # Validate each individual rule entry
    for r in quality:
        rule_name = r.get("rule")
        if rule_name not in VALID_RULES:
            issues.append(err(path, f"Neplatný quality rule `{rule_name}` "
                                    f"(povolené: {sorted(VALID_RULES)})"))
            continue
        # field is required only for field-level rules
        if rule_name not in TABLE_LEVEL_RULES and not r.get("field"):
            issues.append(err(path, f"Quality pravidlo `{rule_name}` chybí `field`"))


def check_regulatory_mapping(path, doc, issues):
    """v3.3 — Check regulatory_mapping covers all 10 required regulations."""
    dawiso = doc.get("x-dawiso", {}).get("data_product", {})
    mapping = dawiso.get("regulatory_mapping")
    if not mapping:
        issues.append(err(path, "x-dawiso.data_product.regulatory_mapping is missing (v3.3)"))
        return

    covered = {entry.get("regulation") for entry in mapping}
    for reg in REQUIRED_REGULATIONS:
        if reg not in covered:
            issues.append(err(path, f"regulatory_mapping is missing regulation: '{reg}' (v3.3)"))

    for entry in mapping:
        reg  = entry.get("regulation", "<unknown>")
        stat = entry.get("status")
        if stat not in VALID_STATUSES:
            issues.append(err(path, f"regulatory_mapping '{reg}' has invalid status '{stat}' "
                                    f"(must be one of: {', '.join(VALID_STATUSES)})"))
        if not entry.get("reason"):
            issues.append(err(path, f"regulatory_mapping '{reg}' is missing a reason (v3.3)"))


def check_ai_act(path, doc, issues):
    """v3.3 — Check AI Act / FRIA section is present and complete."""
    dawiso = doc.get("x-dawiso", {}).get("data_product", {})
    ai = dawiso.get("ai_act")
    if ai is None:
        issues.append(err(path, "x-dawiso.data_product.ai_act block is missing (v3.3)"))
        return
    for field in ["is_ai_input", "is_ai_output", "high_risk_classification",
                  "fria_required", "fria_notes"]:
        if field not in ai:
            issues.append(err(path, f"ai_act.{field} is missing (v3.3)"))


def check_glossary(path, doc, issues):
    """Check FIBO glossary entry is present and populated."""
    glossary = doc.get("x-dawiso", {}).get("glossary_entry", {})
    if not glossary:
        issues.append(err(path, "x-dawiso.glossary_entry block is missing"))
        return
    for field in ["term", "definition", "fibo_class", "fibo_uri", "domain", "steward"]:
        if not glossary.get(field):
            issues.append(err(path, f"glossary_entry.{field} is missing or empty"))


def check_dawiso(path, doc, issues):
    """Check x-dawiso.data_product mandatory fields."""
    dp = doc.get("x-dawiso", {}).get("data_product", {})
    if not dp:
        issues.append(err(path, "x-dawiso.data_product block is missing"))
        return
    for field in ["domain", "business_owner", "product_owner", "data_steward",
                  "data_classification", "lineage", "rules_ko", "retention"]:
        if not dp.get(field):
            issues.append(err(path, f"x-dawiso.data_product.{field} is missing or empty"))


# ── Main ──────────────────────────────────────────────────────────────────────

def validate_file(path):
    issues = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [err(path, f"YAML parse error: {e}")]

    if not isinstance(doc, dict):
        return [err(path, "File is empty or not a valid YAML mapping")]

    check_core(path, doc, issues)
    check_extended_gdpr(path, doc, issues)
    check_fields_compliance(path, doc, issues)
    check_quality(path, doc, issues)
    check_regulatory_mapping(path, doc, issues)
    check_ai_act(path, doc, issues)
    check_glossary(path, doc, issues)
    check_dawiso(path, doc, issues)

    return issues


def main():
    files = [
        f for pattern in CONTRACT_GLOBS
        for f in glob.glob(pattern, recursive=True)
        if ".github" not in f and "node_modules" not in f
    ]

    if not files:
        print("⚠️  No YAML contract files found.")
        sys.exit(0)

    total_files  = len(files)
    total_issues = 0
    report_lines = [
        "═══════════════════════════════════════════════════════════",
        " Nova Banka — Data Contract Validation Report (prompt v3.3)",
        "═══════════════════════════════════════════════════════════",
        "",
    ]

    for path in sorted(files):
        issues = validate_file(path)
        if issues:
            total_issues += len(issues)
            report_lines.append(f"📄 {path}  →  {len(issues)} issue(s)")
            report_lines.extend(issues)
        else:
            report_lines.append(ok(f"{path}  →  all checks passed"))
        report_lines.append("")

    report_lines += [
        "───────────────────────────────────────────────────────────",
        f" Files checked : {total_files}",
        f" Total issues  : {total_issues}",
        "───────────────────────────────────────────────────────────",
    ]

    report = "\n".join(report_lines)
    print(report)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    if total_issues > 0:
        print(f"\n❌ Validation failed — {total_issues} issue(s) found. See {REPORT_PATH}")
        sys.exit(1)
    else:
        print(f"\n✅ All {total_files} contract(s) passed validation.")
        sys.exit(0)


if __name__ == "__main__":
    main()
