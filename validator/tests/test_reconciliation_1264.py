from __future__ import annotations
from .current_policy_helpers import CURRENT_NORM_FILE, CURRENT_NORM, CURRENT_VALIDATOR, CURRENT_KIT, current_norm_path

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_compatibility_revision_lists_are_unique_and_continuous():
    data = json.loads((ROOT / "COMPATIBILITY.json").read_text(encoding="utf-8"))
    for key in ("compatible_normative_revisions", "supported_normative_revisions"):
        values = data[key]
        assert len(values) == len(set(values))
        assert "1.2.62" in values
        assert "1.2.63" in values
        assert "1.2.64" in values
        assert "1.2.66" in values
    supported = data["supported_normative_revisions"]
    expected = [f"1.2.{i}" for i in range(53, int(CURRENT_NORM.split(".")[-1]) + 1)]
    assert supported[-len(expected):] == expected

def test_previous_active_norm_is_archived_and_current_norm_is_unique():
    norm = ROOT / "normative_reference" / "01_normes"
    assert (norm / CURRENT_NORM_FILE).is_file()
    assert (norm / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.66.md").is_file()
    assert (norm / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.64.md").is_file()
    assert (norm / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.63.md").is_file()
