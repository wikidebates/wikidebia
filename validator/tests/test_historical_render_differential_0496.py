from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package, dump


def _legacy_preexisting_fixture(root: Path) -> tuple[Path, Path, Path]:
    create_fr_package(root)
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    debate_page = next(p for p in manifest["pages"] if p["language"] == "fr" and p["page_type"] == "debate")
    arg1_page = next(p for p in manifest["pages"] if p["language"] == "fr" and p.get("page_id") == "A0001")
    arg2_page = next(p for p in manifest["pages"] if p["language"] == "fr" and p.get("page_id") == "A0002")
    for page in (debate_page, arg1_page, arg2_page):
        page["page_origin"] = "preexisting"
    manifest.setdefault("editorial_controls", {})["historical_text_render_validation_mode"] = "differential_preservation_v1"
    dump(manifest_path, manifest)

    debate_path = root / debate_page["file_path"]
    debate_text = debate_path.read_text(encoding="utf-8")
    debate_text = debate_text.replace(
        "|contenu=La mesure X est une mesure pilote.",
        "|contenu=La mesure X est une mesure pilote.\n|avertissements=À développer\n<references />",
        1,
    )
    debate_path.write_text(debate_text, encoding="utf-8")

    arg1_path = root / arg1_page["file_path"]
    arg1_text = arg1_path.read_text(encoding="utf-8")
    old_summary = "La mesure X mutualiserait certains bénéfices et réduirait des coûts collectifs."
    historical_summary = (
        "La {{Lien Wikipédia|article=marchandisation|infobulle=Ancienne infobulle historique}} "
        "peut modifier les échanges économiques."
    )
    arg1_text = arg1_text.replace(old_summary, historical_summary, 1)
    arg1_path.write_text(arg1_text, encoding="utf-8")

    arg2_path = root / arg2_page["file_path"]
    arg2_text = arg2_path.read_text(encoding="utf-8")
    summary_line = next(line for line in arg2_text.splitlines() if line.startswith("|résumé="))
    arg2_text = arg2_text.replace(summary_line + "\n", "", 1)
    arg2_path.write_text(arg2_text, encoding="utf-8")

    # This reproduces the legacy fr_content_lock shape carried by the real
    # revenu_de_base Work: page_origin + selected values, before the explicit
    # historical_text_decisions inventory was introduced.
    from wikidebia_validator.wikicode import parse_template
    intro = parse_template(debate_text).one("introduction")
    dump(root / "data/fr_content_lock.json", {
        "schema": "wikidebia-fr-content-lock-1.0",
        "schema_version": "1.0",
        "debate_id": manifest["debate_id"],
        "debate": {
            "page_origin": "preexisting",
            "introduction": intro,
        },
        "arguments": [
            {"id": "A0001", "page_origin": "preexisting", "summary": historical_summary},
            {"id": "A0002", "page_origin": "preexisting", "summary": None},
        ],
    })
    return debate_path, arg1_path, arg2_path


def test_legacy_preexisting_render_preserves_historical_syntax_without_new_generation_errors(tmp_path: Path):
    debate_path, arg1_path, arg2_path = _legacy_preexisting_fixture(tmp_path)
    report = validate_package(tmp_path, scopes=["wikicode", "editorial"])

    assert not any(
        f.level == "ERROR" and f.code == "WDV-EDT-010" and f.path == str(debate_path.relative_to(tmp_path))
        for f in report.findings
    ), report.to_text()
    assert not any(
        f.level == "ERROR" and f.code == "WDV-MWK-003" and "Sous-partie.avertissements" in f.message
        and f.path == str(debate_path.relative_to(tmp_path))
        for f in report.findings
    ), report.to_text()
    assert not any(
        f.level == "ERROR" and f.code == "WDV-MWK-020" and f.path == str(arg1_path.relative_to(tmp_path))
        for f in report.findings
    ), report.to_text()
    assert not any(
        f.level == "ERROR" and f.code == "WDV-MWK-004" and "résumé" in f.message
        and f.path == str(arg2_path.relative_to(tmp_path))
        for f in report.findings
    ), report.to_text()
    assert not any(
        f.level == "ERROR" and f.code in {"WDV-DOC-005", "WDV-DOC-008"}
        and f.path == str(debate_path.relative_to(tmp_path))
        for f in report.findings
    ), report.to_text()


def test_new_content_still_blocks_references_subsection_warning_unknown_hover_parameter_and_missing_summary(tmp_path: Path):
    create_fr_package(tmp_path)
    debate_path = tmp_path / "output/fr/debate/debate.wiki"
    debate = debate_path.read_text(encoding="utf-8").replace(
        "|contenu=La mesure X est une mesure pilote.",
        "|contenu=La mesure X est une mesure pilote.\n|avertissements=À développer\n<references />",
        1,
    )
    debate_path.write_text(debate, encoding="utf-8")

    arg1 = tmp_path / "output/fr/arguments/A0001.wiki"
    text = arg1.read_text(encoding="utf-8").replace(
        "La mesure X mutualiserait certains bénéfices et réduirait des coûts collectifs.",
        "La {{Lien Wikipédia|article=marchandisation|infobulle=Ancienne infobulle}} modifie les échanges.",
        1,
    )
    arg1.write_text(text, encoding="utf-8")

    arg2 = tmp_path / "output/fr/arguments/A0002.wiki"
    text2 = arg2.read_text(encoding="utf-8")
    summary_line = next(line for line in text2.splitlines() if line.startswith("|résumé="))
    arg2.write_text(text2.replace(summary_line + "\n", "", 1), encoding="utf-8")

    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.level == "ERROR" and f.code == "WDV-EDT-010" for f in report.findings), report.to_text()
    assert any(f.level == "ERROR" and f.code == "WDV-MWK-003" and "Sous-partie.avertissements" in f.message for f in report.findings), report.to_text()
    assert any(f.level == "ERROR" and f.code == "WDV-MWK-020" for f in report.findings), report.to_text()
    assert any(f.level == "ERROR" and f.code == "WDV-MWK-004" and "résumé" in f.message for f in report.findings), report.to_text()
