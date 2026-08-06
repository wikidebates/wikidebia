from pathlib import Path
import hashlib, json

from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package, dump


def _remove_summary(text: str) -> str:
    start = text.index("|résumé=")
    end = text.find("\n|", start)
    return text[:start] + text[end + 1:]


def _package(root: Path):
    create_fr_package(root)
    manifest = json.loads((root / "manifest.json").read_text())
    manifest["translation_status"] = {"en": "deferred"}
    manifest["editorial_controls"] = {
        "creation_date": "2026-07-23",
        "creation_date_policy": "per_page_preserved",
        "individual_review_path": "reviews/individual_review.json",
        "individual_review_report_path": "reports/individual.txt",
        "keyword_vocabulary_path": "data/keyword_vocabulary.json",
        "summary_style_review_path": "reviews/summary_style_review.json",
        "summary_policy_revision": "1.2.40",
        "required_reports": [],
        "debate_documentation": {"min_subsections": 1, "min_references": 0, "reject_singleton_bucket_pattern": True, "profile_rationale": "Profil de test complet."},
        "introduction_references": {"required": True},
        "introduction_review_path": "reviews/introduction_review.json",
        "graph_placement_review_path": "reviews/graph_placement_review.json",
        "legacy_content_preservation": {
            "enabled": True,
            "lock_path": "data/historical_content_lock.json",
            "protected_fields": ["résumé", "initialisation"],
            "source_archive_sha256": "a" * 64,
            "verification_revision": "0.4.43",
            "summary_policy_revision": "1.2.40",
            "source_inventory_path": "data/initial_remote_inventory_fr.json",
        },
    }
    argument_pages = [p for p in manifest["pages"] if p["page_type"] == "argument" and p["language"] == "fr"]
    imported = argument_pages[0]
    imported_path = root / imported["file_path"]
    imported_source = _remove_summary(imported_path.read_text())
    imported_path.write_text(imported_source)
    entries = [{"id": imported["page_id"], "language": "fr", "summary_provenance": "absent_at_import", "initialisation": {"present": False}}]
    for page in argument_pages[1:]:
        path = root / page["file_path"]
        path.write_text(_remove_summary(path.read_text()))
        entries.append({"id": page["page_id"], "language": "fr", "summary_provenance": "new_page_unwritten", "initialisation": {"present": False}})
    inventory = {
        "inventory_version": "1.0", "inventory_mode": "explicit_debate_pages_read_only",
        "debate_id": manifest["debate_id"], "language": "fr", "generated_at": "2026-08-06T00:00:00+00:00",
        "pages": [{"page_id": imported["page_id"], "page_type": "argument", "canonical_title": imported["canonical_title"], "content_sha256": hashlib.sha256(imported_source.encode()).hexdigest(), "revision_id": 42, "status": "published", "content": imported_source}],
        "inventory_sha256": "0" * 64,
    }
    inventory_path = root / "data/initial_remote_inventory_fr.json"
    dump(inventory_path, inventory)
    manifest["editorial_controls"]["legacy_content_preservation"]["source_inventory_sha256"] = hashlib.sha256(inventory_path.read_bytes()).hexdigest()
    dump(root / "manifest.json", manifest)
    dump(root / "data/historical_content_lock.json", {
        "schema_version": "1.1", "summary_policy_revision": "1.2.40", "debate_id": manifest["debate_id"],
        "source_archive": "source.zip", "source_archive_sha256": "a" * 64,
        "protected_fields": ["résumé", "initialisation"], "arguments": entries,
    })
    return manifest, imported, imported_path


def test_absent_at_import_summary_must_be_absent_and_passes(tmp_path: Path):
    _package(tmp_path)
    report = validate_package(tmp_path, scopes=["schema", "wikicode"])
    assert not any(f.code in {"WDV-EDT-027", "WDV-EDT-028", "WDV-MWK-004"} for f in report.findings)


def test_absent_at_import_rejects_mechanical_summary(tmp_path: Path):
    manifest, imported, path = _package(tmp_path)
    text = path.read_text().replace("|avertissements-argument=Argument généré par IA\n", "|avertissements-argument=Argument généré par IA\n|résumé=Cette analyse mène à la conclusion que le titre est vrai.\n")
    path.write_text(text)
    report = validate_package(tmp_path, scopes=["schema", "wikicode"])
    assert any(f.code == "WDV-EDT-028" and f.path == imported["file_path"] for f in report.findings)


def test_new_page_unwritten_rejects_summary_until_status_changes(tmp_path: Path):
    manifest, _, _ = _package(tmp_path)
    page = [p for p in manifest["pages"] if p["page_type"] == "argument" and p["language"] == "fr"][1]
    path = tmp_path / page["file_path"]
    path.write_text(path.read_text().replace("|avertissements-argument=Argument généré par IA\n", "|avertissements-argument=Argument généré par IA\n|résumé=Paraphrase mécanique du titre.\n"))
    report = validate_package(tmp_path, scopes=["schema", "wikicode"])
    assert any(f.code == "WDV-EDT-028" and f.path == page["file_path"] for f in report.findings)


def test_043_rejects_initialisation_lock_that_contradicts_source_inventory(tmp_path: Path):
    manifest, imported, path = _package(tmp_path)
    # La page courante et le verrou s'accordent sur une mauvaise valeur.
    wrong = "Argument pour@999"
    text = path.read_text()
    pos = text.rfind("\n}}")
    path.write_text(text[:pos] + f"\n|initialisation={wrong}" + text[pos:])
    lock_path = tmp_path / "data/historical_content_lock.json"
    lock = json.loads(lock_path.read_text())
    lock["arguments"][0]["initialisation"] = {"present": True, "value": wrong}
    dump(lock_path, lock)
    # L'inventaire autoritatif conserve une autre valeur historique.
    inventory_path = tmp_path / "data/initial_remote_inventory_fr.json"
    inventory = json.loads(inventory_path.read_text())
    right = "Argument pour@42"
    source = inventory["pages"][0]["content"]
    pos = source.rfind("\n}}")
    source = source[:pos] + f"\n|initialisation={right}" + source[pos:]
    inventory["pages"][0]["content"] = source
    inventory["pages"][0]["content_sha256"] = hashlib.sha256(source.encode()).hexdigest()
    dump(inventory_path, inventory)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    manifest["editorial_controls"]["legacy_content_preservation"]["source_inventory_sha256"] = hashlib.sha256(inventory_path.read_bytes()).hexdigest()
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["schema", "wikicode"])
    assert any(f.code == "WDV-EDT-027" and "Verrou d’initialisation incohérent" in f.message for f in report.findings)
