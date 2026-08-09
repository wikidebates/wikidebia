from pathlib import Path

from wikidebia_validator import __version__


def test_validator_metadata_reports_0414():
    assert __version__ == "0.4.63"


def test_norm_1214_is_declared_compatible():
    root = Path(__file__).resolve().parents[1]
    text = (root / "COMPATIBILITY.json").read_text(encoding="utf-8")
    assert '"implemented_normative_revision": "1.2.59"' in text
    assert '"1.2.18"' in text
