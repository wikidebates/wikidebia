from pathlib import Path

from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package


def test_fr_package_valid(tmp_path: Path):
    create_fr_package(tmp_path)
    report = validate_package(tmp_path)
    assert report.errors == 0, report.to_text()


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
    assert report.errors == 0, report.to_text()
