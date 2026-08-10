import json
from .current_policy_helpers import CURRENT_NORM_FILE, CURRENT_NORM, CURRENT_VALIDATOR, CURRENT_KIT, current_norm_path
from pathlib import Path

from wikidebia_validator import __version__


def test_validator_metadata_reports_0414():
    assert __version__ == CURRENT_VALIDATOR


def test_norm_1214_is_declared_compatible():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "COMPATIBILITY.json").read_text(encoding="utf-8"))
    assert data["implemented_normative_revision"] == CURRENT_NORM
    assert "1.2.18" in data["compatible_normative_revisions"]
