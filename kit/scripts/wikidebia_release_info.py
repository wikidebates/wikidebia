from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load_json(name: str) -> dict[str, Any]:
    data = json.loads((ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Objet JSON attendu dans {name}")
    return data


VERSIONS = _load_json("VERSIONS.json")
CAPABILITY_MANIFEST = _load_json("CAPABILITIES.json")
NORM_VERSION = str(VERSIONS["norm"])
VALIDATOR_VERSION = str(VERSIONS["validator"])
REQUIRED_VALIDATOR_VERSION = VALIDATOR_VERSION  # alias de provenance historique
KIT_VERSION = str(VERSIONS["kit"])

VALIDATOR_REPORT_SCHEMA = "wikidebia-validator-report-1.0"
PUBLICATION_PLAN_SCHEMA = "wikidebia-publication-plan-1.0"
PUBLICATION_PLAN_SCHEMA_VERSION = "1.0"


def accepted_schema_pairs(kind: str) -> set[tuple[str, str]]:
    rows = ((CAPABILITY_MANIFEST.get("accepts") or {}).get(kind) or [])
    result: set[tuple[str, str]] = set()
    for row in rows:
        if isinstance(row, str):
            result.add((row, ""))
            continue
        if not isinstance(row, dict):
            continue
        schema = str(row.get("schema") or "")
        versions = row.get("schema_versions") or [str(row.get("schema_version") or "")]
        for version in versions:
            result.add((schema, str(version or "")))
    return result


def schema_is_supported(kind: str, schema: str, schema_version: str = "") -> bool:
    accepted = accepted_schema_pairs(kind)
    return (schema, schema_version) in accepted or (schema, "") in accepted


def validator_report_is_compatible(report: dict[str, Any]) -> bool:
    schema = str(report.get("schema") or "")
    schema_version = str(report.get("schema_version") or "")
    if not schema:
        # Legacy validator reports predate the explicit report schema. They are
        # accepted only when their shape proves the stable report contract.
        return all(key in report for key in ("validator_version", "result", "summary"))
    return schema_is_supported("validator_report", schema, schema_version)


def canonical_publication_plan_schema(plan: dict[str, Any]) -> tuple[str, str]:
    schema = str(plan.get("schema") or "")
    version = str(plan.get("schema_version") or "")
    if schema:
        return schema, version
    legacy = str(plan.get("plan_version") or "")
    # Historical publication plans encoded the kit release in the schema name.
    # Their data shape remained the publication-plan 1.0 format, so normalize
    # that producer-coupled label at the input boundary.
    if re.fullmatch(r"wikidebia-publication-plan-\d+\.\d+\.\d+", legacy):
        return PUBLICATION_PLAN_SCHEMA, PUBLICATION_PLAN_SCHEMA_VERSION
    return legacy, version


def publication_plan_is_compatible(plan: dict[str, Any]) -> bool:
    schema, version = canonical_publication_plan_schema(plan)
    return schema_is_supported("publication_plan", schema, version)


def require_validator_report(report: dict[str, Any], error_type: type[Exception], label: str = "rapport du validateur") -> None:
    if not validator_report_is_compatible(report):
        schema = str(report.get("schema") or "legacy/unknown")
        version = str(report.get("schema_version") or "")
        raise error_type(f"Schéma incompatible pour {label} : {schema} {version}".strip())
