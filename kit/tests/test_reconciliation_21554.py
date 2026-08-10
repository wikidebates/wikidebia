import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_validator_publication_metadata_regression_gates_are_declared():
    manifest = json.loads((ROOT / "KIT_MANIFEST.json").read_text(encoding="utf-8"))
    gates = set(manifest["regression_gates"])
    assert "validator_english_initialization_source_projection_regression" in gates
    assert "validator_english_creation_date_source_equality_regression" in gates
    assert manifest["version"] == "2.15.54"
    assert manifest["validator_version"] == "0.4.73"
    assert manifest["normative_revision"] == "1.2.70"
