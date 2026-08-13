from pathlib import Path
import json

from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package


def test_old_minimal_fr_fixture_is_subject_to_current_cumulative_rules(tmp_path: Path):
    create_fr_package(tmp_path)
    report = validate_package(tmp_path)
    codes = {f.code for f in report.findings if f.level == "ERROR"}
    assert "WDV-EDT-032" in codes
    assert "WDV-WF-005" in codes


def test_unknown_empty_and_wrong_relation_detected(tmp_path: Path):
    create_fr_package(tmp_path)
    p = tmp_path / "output/fr/arguments/A0001.wiki"
    content = p.read_text()
    content = content.replace("|résumé=", "|paramètre-inconnu=x\n|résumé=\n|objections={{Objection\n|page=Page fantôme\n|titre-affiché=Fantôme\n}}\n|résumé-bis=")
    p.write_text(content, encoding="utf-8")
    report = validate_package(tmp_path, scopes=["wikicode"])
    codes = {f.code for f in report.findings if f.level == "ERROR"}
    assert "WDV-MWK-003" in codes
    assert "WDV-MWK-005" in codes
    assert "WDV-MWK-008" in codes


def test_premature_interlanguage_detected(tmp_path: Path):
    create_fr_package(tmp_path)
    p = tmp_path / "output/fr/arguments/A0001.wiki"
    content = p.read_text().replace("|date-création=", "|interlangue={{Lien interlangue\n|langue=en\n|page=English title\n}}\n|date-création=")
    p.write_text(content, encoding="utf-8")
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.code == "WDV-MWK-011" for f in report.findings)


def test_video_author_may_be_omitted_in_wikicode(tmp_path: Path):
    create_fr_package(tmp_path)
    p = tmp_path / "output/fr/debate/debate.wiki"
    content = p.read_text(encoding="utf-8").replace(
        "|débats-connexes=",
        "|vidéographie-ni-pour-ni-contre={{Référence vidéographique\n"
        "|titre=Vidéo dont le responsable éditorial n'est pas identifié\n"
        "|lien=https://example.org/video\n"
        "}}\n|débats-connexes=",
    ) if "|débats-connexes=" in p.read_text(encoding="utf-8") else p.read_text(encoding="utf-8").replace(
        "|rubriques=",
        "|vidéographie-ni-pour-ni-contre={{Référence vidéographique\n"
        "|titre=Vidéo dont le responsable éditorial n'est pas identifié\n"
        "|lien=https://example.org/video\n"
        "}}\n|rubriques=",
    )
    p.write_text(content, encoding="utf-8")
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert not any(f.code == "WDV-MWK-012" and "auteurs" in f.message for f in report.findings), report.to_text()


def test_french_reference_typography_and_date_language_detected(tmp_path: Path):
    create_fr_package(tmp_path)
    p = tmp_path / "output/fr/debate/debate.wiki"
    content = p.read_text(encoding="utf-8").replace(
        "La mesure X est une mesure pilote.",
        "La mesure X est une mesure pilote.<ref>[https://example.org Source], April 3, 2026.</ref>",
    )
    p.write_text(content, encoding="utf-8")
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.code == "WDV-MWK-014" for f in report.findings), report.to_text()


def test_french_debate_constructed_value_is_active(tmp_path):
    from .helpers import create_fr_package
    from wikidebia_validator.validator import validate_package

    root = create_fr_package(tmp_path)
    debate = root / "output/fr/debate/debate.wiki"
    assert "|avancement=Débat construit" in debate.read_text(encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert not any(f.code == "WDV-MWK-003" and "avancement" in f.message for f in report.findings), report.to_text()



def _make_preexisting_empty_objections_fixture(tmp_path: Path, *, present: bool) -> Path:
    root = create_fr_package(tmp_path)
    argument_path = root / "output/fr/arguments/A0001.wiki"
    argument = argument_path.read_text(encoding="utf-8").replace(
        "|rubriques=",
        "|objections=\n|rubriques=",
        1,
    )
    argument_path.write_text(argument, encoding="utf-8")

    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    page = next(row for row in manifest["pages"] if row.get("page_id") == "A0001")
    page["page_origin"] = "preexisting"
    import hashlib
    page["sha256"] = hashlib.sha256(argument_path.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lock = {
        "schema": "wikidebia-fr-content-lock-1.0",
        "schema_version": "1.1",
        "debate_id": "exemple",
        "debate": {"page_origin": "new", "source_parameter_presence": {}},
        "arguments": [
            {
                "id": "A0001",
                "page_origin": "preexisting",
                "source_parameter_presence": {
                    "objections": {"present": present}
                },
            }
        ],
    }
    lock_path = root / "data/fr_content_lock.json"
    lock_path.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return root


def test_historical_present_empty_top_level_parameter_is_allowed(tmp_path: Path):
    root = _make_preexisting_empty_objections_fixture(tmp_path, present=True)
    report = validate_package(root, scopes=["wikicode"])
    assert not any(
        f.code == "WDV-MWK-005" and "objections" in f.message
        for f in report.findings
    ), report.to_text()


def test_empty_top_level_parameter_without_historical_presence_remains_blocked(tmp_path: Path):
    root = _make_preexisting_empty_objections_fixture(tmp_path, present=False)
    report = validate_package(root, scopes=["wikicode"])
    assert any(
        f.code == "WDV-MWK-005" and "objections" in f.message
        for f in report.findings
    ), report.to_text()
