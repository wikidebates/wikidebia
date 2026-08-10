from __future__ import annotations
from .current_policy_helpers import CURRENT_NORM_FILE, CURRENT_NORM, CURRENT_VALIDATOR, CURRENT_KIT, current_norm_path

import json
from pathlib import Path

from wikidebia_validator.report import Report
from wikidebia_validator.versioning import REPORT_SCHEMA, REPORT_SCHEMA_VERSION, VALIDATOR_VERSION

ROOT = Path(__file__).resolve().parents[1]


def test_report_declares_stable_schema_separate_from_producer_version():
    payload = Report(VALIDATOR_VERSION, ".", ["schema"]).to_dict()
    assert payload["schema"] == REPORT_SCHEMA
    assert payload["schema_version"] == REPORT_SCHEMA_VERSION
    assert payload["producer"]["version"] == VALIDATOR_VERSION


def test_compatibility_revision_lists_are_derived_not_hand_maintained():
    data = json.loads((ROOT / "COMPATIBILITY.json").read_text(encoding="utf-8"))
    assert isinstance(data["compatible_normative_revisions"], list)
    assert isinstance(data["supported_normative_revisions"], list)
    assert data["compatibility_list_generation"]["used_as_feature_flag"] is False


def test_active_norm_is_separate_from_history_and_contains_no_addendum_headings():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    active = ROOT / "normative_reference" / "01_normes" / f"WIKIDEBIA_NORME_CONSOLIDEE_{versions['norm']}.md"
    text = active.read_text(encoding="utf-8")
    assert "## Addendum " not in text
    assert "## Correction 1.2." not in text
    assert "## Architecture de compatibilité active" in text
    parent = ROOT / "normative_reference" / "01_normes" / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.70.md"
    assert parent.is_file()
