import json
from pathlib import Path

from wikidebia_validator.editorial import validate_introduction_review_data


def test_norm_128_catalog_all_source_labels_resolve():
    root = Path(__file__).resolve().parents[1] / "normative_reference"
    data = json.loads((root / "01_normes/requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    aliases = data["source_aliases"]
    used = {label for req in data["requirements"] for label in req.get("sources", [])}
    assert used <= set(aliases)
    for paths in aliases.values():
        assert paths
        assert all((root / rel).is_file() for rel in paths)
    for req in data["requirements"]:
        assert all((root / rel).is_file() for rel in req.get("normative_files", []))


def test_introduction_review_revision_is_trace_only():
    review = {"normative_revision": "1.2.7", "entries": []}
    issues = validate_introduction_review_data(review, {}, norm="1.2.8")
    assert not any(i["reason"] == "wrong_normative_revision" for i in issues)


def test_schema_has_no_norm_version_activation_condition():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "src/wikidebia_validator/schemas/debate_package.schema.json").read_text(encoding="utf-8"))
    assert not data.get("allOf")


def test_active_examples_use_current_revision_and_language():
    package_root = Path(__file__).resolve().parents[1]
    intro = json.loads((package_root / "examples/introduction_review.example.json").read_text(encoding="utf-8"))
    style = json.loads((package_root / "examples/summary_style_review.example.json").read_text(encoding="utf-8"))
    assert intro["normative_revision"] == "1.2.66"
    assert style["normative_revision"] == "1.2.66"
    en = next(entry for entry in intro["entries"] if entry["language"] == "en")
    assert en["documentation_family_notes"]["bibliography"].startswith("Broad syntheses")
    root = package_root / "normative_reference"
    decisions = (root / "00_sources_reference/DECISIONS_CONVERSATION_CONSOLIDEES.md").read_text(encoding="utf-8")
    assert "Les titres canoniques anglais sont verrouillés" in decisions
    assert "Aucun lien interlangue provisoire n’est généré pendant `translation_status.en=deferred`" in decisions
