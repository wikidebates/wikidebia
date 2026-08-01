from pathlib import Path
import json

from wikidebia_validator.cli import main
from wikidebia_validator.validator import validate_package
from .helpers import create_graph_package, dump


def test_schema_violation(tmp_path: Path):
    create_graph_package(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    manifest["unexpected"] = True
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["schema"])
    assert any(f.code == "WDV-SCH-003" for f in report.findings)


def test_cli_json_output(tmp_path: Path):
    create_graph_package(tmp_path)
    output = tmp_path / "report.json"
    rc = main(["validate", str(tmp_path), "--format", "json", "--json-output", str(output)])
    assert rc == 0
    data = json.loads(output.read_text())
    assert data["result"] in {"passed", "passed_with_warnings"}


def test_video_source_without_author_requires_verification_note():
    from wikidebia_validator.schema_validation import SchemaStore

    store = SchemaStore()
    base = {
        "source_registry_version": "1.0",
        "debate_id": "exemple",
        "sources": [{
            "id": "S00001",
            "type": "videography",
            "language": "fr",
            "metadata": {
                "authors": [], "article": None, "work": None, "volume": None,
                "issue": None, "location": None, "publisher": None, "place": None,
                "date": None, "link": "https://example.org/video", "page": None,
                "site": None, "title": "Vidéo documentaire",
            },
            "verification": {
                "status": "verified", "verified_at": "2026-07-23T18:00:00+02:00",
                "primary_source": False, "notes": [],
            },
            "usage": [{"page_id": "A0001", "language": "fr", "role": "supports_summary"}],
            "deduplication_key": "video-documentaire",
        }],
    }
    assert store.validate(base, "source_registry.schema.json")
    base["sources"][0]["verification"]["notes"] = [
        "La page, la description et les crédits ont été vérifiés sans permettre d'identifier un responsable éditorial."
    ]
    assert not store.validate(base, "source_registry.schema.json")


def _editorial_controls_124():
    return {
        "creation_date": "2026-07-23",
        "individual_review_path": "reports/individual_review.json",
        "individual_review_report_path": "reports/individual_review_report.json",
        "keyword_vocabulary_path": "data/keyword_vocabulary.json",
        "required_reports": [],
        "debate_documentation": {
            "min_subsections": 1,
            "min_references": 0,
            "reject_singleton_bucket_pattern": True,
            "profile_rationale": "Profil local minimal pour le paquet d'exemple.",
        },
        "introduction_references": {"required": True, "min_subsections": 1},
        "introduction_review_path": "reports/introduction_review.json",
    }


def test_norm_124_schema_requires_introduction_review_and_profile_rationale(tmp_path: Path):
    create_graph_package(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    manifest["normative_versions"]["consolidated_norm"] = "1.2.4"
    controls = _editorial_controls_124()
    controls.pop("introduction_review_path")
    controls["debate_documentation"].pop("profile_rationale")
    manifest["editorial_controls"] = controls
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["schema"])
    assert any(f.code == "WDV-SCH-003" for f in report.findings)


def test_norm_124_schema_accepts_declared_introduction_review_and_rationale(tmp_path: Path):
    create_graph_package(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    manifest["normative_versions"]["consolidated_norm"] = "1.2.4"
    manifest["editorial_controls"] = _editorial_controls_124()
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["schema"])
    assert not any(f.code == "WDV-SCH-003" for f in report.findings)



def test_norm_1220_schema_requires_graph_placement_review_path(tmp_path: Path):
    create_graph_package(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    manifest["normative_versions"]["consolidated_norm"] = "1.2.20"
    manifest["editorial_controls"] = _editorial_controls_124()
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["schema"])
    assert any(f.code == "WDV-SCH-003" for f in report.findings)


def test_norm_1220_schema_accepts_graph_placement_review_path(tmp_path: Path):
    create_graph_package(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    manifest["normative_versions"]["consolidated_norm"] = "1.2.20"
    controls = _editorial_controls_124()
    controls["graph_placement_review_path"] = "reports/graph_placement_review.json"
    manifest["editorial_controls"] = controls
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["schema"])
    assert not any(f.code == "WDV-SCH-003" for f in report.findings)
