"""
Prepare and optionally send validated data contracts to Dawiso.

This script is designed for GitHub Actions after contract validation passes.
It reads only changed YAML/YML contracts from the current push, maps them into a
stable JSON payload, and can either:
1. export the payload as an artifact, or
2. POST it to a Dawiso ingestion endpoint.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml


REPO_ROOT = Path.cwd()
PAYLOAD_PATH = Path(os.getenv("DAWISO_PAYLOAD_PATH", "dawiso_payload.json"))
EVENT_NAME = os.getenv("GITHUB_EVENT_NAME", "")
EVENT_PATH = os.getenv("GITHUB_EVENT_PATH", "")
BEFORE_SHA = os.getenv("GITHUB_EVENT_BEFORE", "")
AFTER_SHA = os.getenv("GITHUB_SHA", "")
TEAM_MAPPING = {
    "team1-digi": "Team - Digi Prodej",
    "team2-Data-Governance": "Team - Data Governance &EA",
    "team3-client-service": "Team - Obsluha klienta",
    "team4-steering-data": "Team - Steering Data",
    "team5-esg-risk": "Team - Risk ESG",
    "team6-strategy": "Team - Strategy",
    "team7-gen-ai": "Team - ICM Gen AI",
    "team8-investment-banking": "Team - Investment Banking",
}


def is_contract_file(path_str: str) -> bool:
    path = Path(path_str)
    return (
        path.suffix.lower() in {".yml", ".yaml"}
        and ".github" not in path.parts
        and "_template" not in path.parts
    )


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def load_event_before_sha() -> str:
    if BEFORE_SHA:
        return BEFORE_SHA
    if not EVENT_PATH:
        return ""
    try:
        with open(EVENT_PATH, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload.get("before", "")
    except (OSError, json.JSONDecodeError):
        return ""


def list_all_contracts() -> list[str]:
    tracked = run_git("ls-files").splitlines()
    return sorted(path for path in tracked if is_contract_file(path))


def changed_contracts(before_sha: str, after_sha: str) -> tuple[list[str], list[str]]:
    if not before_sha or set(before_sha) == {"0"}:
        return list_all_contracts(), []

    diff_output = run_git("diff", "--name-status", before_sha, after_sha)
    upserts: set[str] = set()
    deletes: set[str] = set()

    for line in diff_output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]

        if status.startswith("R") and len(parts) >= 3:
            old_path, new_path = parts[1], parts[2]
            if is_contract_file(old_path):
                deletes.add(old_path)
            if is_contract_file(new_path):
                upserts.add(new_path)
            continue

        if len(parts) < 2:
            continue

        path = parts[1]
        if not is_contract_file(path):
            continue

        if status == "D":
            deletes.add(path)
        else:
            upserts.add(path)

    return sorted(upserts), sorted(deletes)


def normalize_schema(schema: object) -> list[dict]:
    if isinstance(schema, dict):
        return [schema]
    if isinstance(schema, list):
        return [item for item in schema if isinstance(item, dict)]
    return []


def compact_list(values: Iterable[object]) -> list[object]:
    seen = []
    for value in values:
        if value in (None, "", [], {}):
            continue
        if value not in seen:
            seen.append(value)
    return seen


def build_databricks_paths(servers: dict) -> list[str]:
    paths = []
    for server_name, details in (servers or {}).items():
        if not isinstance(details, dict):
            continue
        catalog = details.get("catalog")
        schema = details.get("schema")
        table = details.get("table")
        if catalog and schema and table:
            paths.append(f"{server_name}:{catalog}.{schema}.{table}")
    return paths


def parse_contract(path_str: str) -> dict:
    team_folder = Path(path_str).parts[0] if Path(path_str).parts else ""

    with open(path_str, "r", encoding="utf-8") as handle:
        doc = yaml.safe_load(handle) or {}

    info = doc.get("info", {})
    x_reg = info.get("x-regulatory", {})
    x_dawiso = doc.get("x-dawiso", {})
    data_product = x_dawiso.get("data_product", {})
    contact = doc.get("contact", {})
    servers = doc.get("servers", {})
    schemas = normalize_schema(doc.get("schema"))

    fields = []
    for schema in schemas:
        fields.extend(schema.get("fields", []))

    pii_fields = [
        field for field in fields
        if isinstance(field, dict) and field.get("x-compliance", {}).get("is_pii") is True
    ]

    legal_bases = compact_list(
        field.get("x-compliance", {}).get("legal_basis")
        for field in pii_fields
        if isinstance(field, dict)
    )

    upstream = data_product.get("lineage", {}).get("upstream", []) or []
    downstream = data_product.get("lineage", {}).get("downstream", []) or []
    quality_rules = doc.get("quality", []) or []

    payload = {
        "contract_path": path_str,
        "source_team": team_folder,
        "target_dawiso_team": TEAM_MAPPING.get(team_folder),
        "contract_id": doc.get("id"),
        "title": info.get("title"),
        "name": info.get("name"),
        "description": info.get("description"),
        "version": info.get("version"),
        "status": info.get("status"),
        "product_type": info.get("product_type"),
        "owner": doc.get("owner"),
        "contact": {
            "name": contact.get("name"),
            "email": contact.get("email"),
        },
        "domain": data_product.get("domain"),
        "business_owner": data_product.get("business_owner"),
        "product_owner": data_product.get("product_owner"),
        "data_steward": data_product.get("data_steward"),
        "classification": data_product.get("classification"),
        "data_classification": data_product.get("data_classification"),
        "tags": data_product.get("tags", []) or [],
        "regulatory_framework": x_reg.get("regulatory_framework"),
        "gdpr_relevant": x_reg.get("gdpr_relevant"),
        "critical_data_element": x_reg.get("critical_data_element"),
        "servers": servers,
        "databricks_paths": build_databricks_paths(servers),
        "schema_names": compact_list(schema.get("name") for schema in schemas),
        "field_count": len(fields),
        "pii_field_count": len(pii_fields),
        "pii_share": round((len(pii_fields) / len(fields)), 4) if fields else 0.0,
        "legal_bases": legal_bases,
        "quality_rule_count": len(quality_rules),
        "quality_rule_types": compact_list(rule.get("rule") for rule in quality_rules),
        "upstream": upstream,
        "downstream": downstream,
        "source_repository": os.getenv("GITHUB_REPOSITORY"),
        "source_commit": AFTER_SHA,
    }
    return payload


def write_summary(upserts: list[dict], deletes: list[str], payload_path: Path, mode: str) -> None:
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    lines = [
        "## Dawiso Sync",
        f"- Mode: `{mode}`",
        f"- Upserts: `{len(upserts)}`",
        f"- Deletes: `{len(deletes)}`",
        f"- Payload: `{payload_path}`",
    ]

    if upserts:
        lines.append("")
        lines.append("### Upserted Contracts")
        lines.extend(f"- `{item['contract_path']}`" for item in upserts)

    if deletes:
        lines.append("")
        lines.append("### Deleted Contracts")
        lines.extend(f"- `{path}`" for path in deletes)

    with open(summary_path, "a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def send_payload(payload: dict) -> None:
    api_url = os.getenv("DAWISO_API_URL", "").strip()
    api_token = os.getenv("DAWISO_API_TOKEN", "").strip()

    if not api_url or not api_token:
        raise RuntimeError(
            "DAWISO_API_URL / DAWISO_API_TOKEN are required for API mode."
        )

    timeout = int(os.getenv("DAWISO_TIMEOUT_SECONDS", "30"))
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        api_url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "User-Agent": "github-actions-dawiso-sync",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_body = response.read().decode("utf-8", errors="replace")
            print(f"Dawiso sync HTTP {response.status}")
            if response_body:
                print(response_body[:2000])
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Dawiso sync failed with HTTP {exc.code}: {error_body[:2000]}"
        ) from exc


def main() -> int:
    if EVENT_NAME and EVENT_NAME != "push":
        print(f"Skipping Dawiso sync for unsupported event '{EVENT_NAME}'.")
        return 0

    before_sha = load_event_before_sha()
    after_sha = AFTER_SHA or "HEAD"
    upsert_paths, delete_paths = changed_contracts(before_sha, after_sha)

    if not upsert_paths and not delete_paths:
        print("No changed contract files detected.")
        return 0

    upserts = [parse_contract(path) for path in upsert_paths if Path(path).exists()]
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": os.getenv("GITHUB_REPOSITORY"),
        "branch": os.getenv("GITHUB_REF_NAME"),
        "commit": AFTER_SHA,
        "upserts": upserts,
        "deletes": delete_paths,
    }

    PAYLOAD_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote payload to {PAYLOAD_PATH}")

    mode = os.getenv("DAWISO_SYNC_MODE", "").strip().lower()
    if not mode:
        mode = "api" if os.getenv("DAWISO_API_URL") and os.getenv("DAWISO_API_TOKEN") else "export"

    write_summary(upserts, delete_paths, PAYLOAD_PATH, mode)

    if mode == "export":
        print("Export mode enabled; skipping Dawiso API call.")
        return 0

    if mode != "api":
        print(f"Unsupported DAWISO_SYNC_MODE '{mode}'. Use 'export' or 'api'.")
        return 1

    send_payload(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
