from __future__ import annotations

import hashlib
import json
from pathlib import Path

from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package, dump


FR_ARGUMENT_PROTECTED = (
    "initialisation", "nom", "avertissements-titre", "avertissements-argument",
    "avertissements-résumé", "avertissements-références",
    "avertissements-justifications", "avertissements-objections",
    "débat-détaillé", "interlangue", "date-création",
)


def _states_from_text(text: str, *, force_absent_argument_warning: bool = False):
    from wikidebia_validator.wikicode import parse_template
    tmpl = parse_template(text)
    out = {}
    for name in FR_ARGUMENT_PROTECTED:
        if force_absent_argument_warning and name == "avertissements-argument":
            out[name] = {"present": False, "value": None}
        else:
            value = tmpl.one(name)
            out[name] = {"present": value is not None, "value": value}
    return out


def _activate_1250_manifest(root: Path):
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    manifest.setdefault("normative_versions", {})["consolidated_norm"] = "1.2.50"
    manifest["normative_versions"]["validator"] = "0.4.53"
    dump(root / "manifest.json", manifest)
    return manifest


def _attach_historical_inventory(root: Path, *, page_id: str, page_type: str, content: str, allowed_deletions=None):
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    inventory_path = root / "data/initial_remote_inventory_fr.json"
    inventory = {
        "inventory_version": "1.0",
        "inventory_mode": "explicit_debate_pages_read_only",
        "debate_id": manifest["debate_id"],
        "language": "fr",
        "generated_at": "2026-08-07T00:00:00+00:00",
        "pages": [{
            "page_id": page_id,
            "page_type": page_type,
            "canonical_title": next(p["canonical_title"] for p in manifest["pages"] if p["page_id"] == page_id),
            "revision_id": 42,
            "status": "published",
            "content_sha256": hashlib.sha256(content.encode()).hexdigest(),
            "content": content,
        }],
        "inventory_sha256": "0" * 64,
    }
    dump(inventory_path, inventory)
    cfg = manifest.setdefault("editorial_controls", {}).setdefault("legacy_content_preservation", {})
    cfg.update({
        "enabled": True,
        "lock_path": "data/historical_content_lock.json",
        "protected_fields": ["all-existing-parameters"],
        "source_archive_sha256": "a" * 64,
        "verification_revision": "0.4.53",
        "source_inventory_path": "data/initial_remote_inventory_fr.json",
        "source_inventory_sha256": hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
        "historical_parameter_restoration": True,
    })
    dump(root / "manifest.json", manifest)
    lock = {
        "schema_version": "1.2",
        "debate_id": manifest["debate_id"],
        "source_archive": "source.zip",
        "source_archive_sha256": "a" * 64,
        "protected_fields": ["all-existing-parameters"],
        "arguments": [],
        "allowed_parameter_deletions": allowed_deletions or [],
    }
    if page_type == "argument":
        lock["arguments"].append({
            "id": page_id,
            "language": "fr",
            "summary_provenance": "generated_after_import",
            "initialisation": {"present": False},
            "nom": {"present": False},
        })
    dump(root / "data/historical_content_lock.json", lock)


def test_existing_argument_top_level_warning_cannot_disappear(tmp_path: Path):
    create_fr_package(tmp_path)
    _activate_1250_manifest(tmp_path)
    page = json.loads((tmp_path / "manifest.json").read_text())["pages"][1]
    current = (tmp_path / page["file_path"]).read_text(encoding="utf-8")
    source = current.replace("{{Argument\n", "{{Argument\n|avertissements-titre=Titre peu clair\n", 1)
    _attach_historical_inventory(tmp_path, page_id=page["page_id"], page_type="argument", content=source)
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.code == "WDV-EDT-030" and f.details.get("parameter") == "avertissements-titre" for f in report.findings)


def test_existing_debate_top_level_warning_cannot_disappear(tmp_path: Path):
    create_fr_package(tmp_path)
    _activate_1250_manifest(tmp_path)
    page = json.loads((tmp_path / "manifest.json").read_text())["pages"][0]
    current = (tmp_path / page["file_path"]).read_text(encoding="utf-8")
    source = current.replace("|avancement=", "|avertissements-titre=Titre historique\n|avancement=", 1)
    _attach_historical_inventory(tmp_path, page_id=page["page_id"], page_type="debate", content=source)
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.code == "WDV-EDT-030" and f.details.get("parameter") == "avertissements-titre" for f in report.findings)


def test_explicit_page_parameter_deletion_is_the_only_generic_exception(tmp_path: Path):
    create_fr_package(tmp_path)
    _activate_1250_manifest(tmp_path)
    page = json.loads((tmp_path / "manifest.json").read_text())["pages"][1]
    current = (tmp_path / page["file_path"]).read_text(encoding="utf-8")
    source = current.replace("{{Argument\n", "{{Argument\n|avertissements-titre=Titre peu clair\n", 1)
    allowed = [{
        "page_id": page["page_id"], "language": "fr", "parameter": "avertissements-titre",
        "owner_decision": "Suppression explicitement décidée pour ce test de non-régression.",
        "owner_decision_recorded_at": "2026-08-07",
    }]
    _attach_historical_inventory(tmp_path, page_id=page["page_id"], page_type="argument", content=source, allowed_deletions=allowed)
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert not any(f.code == "WDV-EDT-030" and f.details.get("parameter") == "avertissements-titre" for f in report.findings)


def test_ai_creation_marker_cannot_be_retroactively_added_to_preexisting_argument(tmp_path: Path):
    create_fr_package(tmp_path)
    manifest = _activate_1250_manifest(tmp_path)
    page = manifest["pages"][1]
    text = (tmp_path / page["file_path"]).read_text(encoding="utf-8")
    page["page_origin"] = "preexisting"
    page["preserved_parameters"] = _states_from_text(text, force_absent_argument_warning=True)
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(
        f.code == "WDV-MWK-023" and "avertissements-argument" in f.message and "ajouté" in f.message
        for f in report.findings
    )
