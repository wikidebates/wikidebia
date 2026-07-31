from pathlib import Path
import json

from wikidebia_validator.graph import contextual_title_issues
from wikidebia_validator.validator import validate_package
from tests.helpers import create_fr_package, dump
from tests.test_norm_120 import _activate_120, _insert_link


def _activate_122(root: Path):
    manifest, registry = _activate_120(root)
    manifest["normative_versions"]["consolidated_norm"] = "1.2.2"
    manifest["normative_versions"]["validator"] = "0.4.5"
    registry["schema"]["validator_version"] = "0.4.5"
    dump(root / "manifest.json", manifest)
    dump(root / "data/registre_debat.json", registry)
    return manifest, registry


def test_norm_122_initial_contextual_title_is_strong_issue():
    assert contextual_title_issues("Cette conception affaiblit le raisonnement", "fr", "1.2.2") == ["initial_contextual_referent"]
    assert contextual_title_issues("Ce que montrent les réplications reste contesté", "fr", "1.2.2") == []


def test_norm_122_internal_contextual_title_is_review_signal():
    assert contextual_title_issues("Plusieurs échecs sur ce protocole réduisent sa valeur", "fr", "1.2.2") == ["possible_contextual_referent"]
    assert contextual_title_issues("Plusieurs échecs sur le protocole programme de contrôle croisé réduisent sa valeur", "fr", "1.2.2") == []


def test_norm_122_ignores_em_dash_inside_inline_reference(tmp_path: Path):
    root = create_fr_package(tmp_path)
    _, registry = _activate_122(root)
    _insert_link(root / "output/fr/debate/debate.wiki", registry["debate"]["pages"]["en"]["canonical_title"])
    page = root / "output/fr/debate/debate.wiki"
    page.write_text(page.read_text(encoding="utf-8").replace(
        "La mesure X est une mesure pilote.",
        "La mesure X est une mesure pilote<ref>Titre cité — sous-titre — édition.</ref>.",
    ), encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert not any(f.code == "WDV-MWK-015" for f in report.findings), report.to_text()


def test_norm_122_requires_direct_interlanguage(tmp_path: Path):
    root = create_fr_package(tmp_path)
    _activate_122(root)
    report = validate_package(root, scopes=["wikicode"])
    assert any(f.code == "WDV-MWK-011" for f in report.findings), report.to_text()
