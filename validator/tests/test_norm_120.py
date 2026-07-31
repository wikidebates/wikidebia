from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator.graph import contextual_title_issues
from wikidebia_validator.validator import validate_package
from wikidebia_validator.wikicode import TOP
from .helpers import create_fr_package, create_graph_package, dump


def _activate_120(root: Path) -> tuple[dict, dict]:
    manifest_path = root / "manifest.json"
    registry_path = root / "data/registre_debat.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    manifest["normative_versions"]["consolidated_norm"] = "1.2.0"
    manifest["normative_versions"]["validator"] = "0.4.0"
    registry["schema"]["validator_version"] = "0.4.0"
    registry["debate"]["pages"]["en"].update({
        "canonical_title": "Should measure X be adopted?",
        "title_status": "locked",
    })
    for node, canonical, displayed in zip(
        registry["graph"]["nodes"],
        ["Measure X would produce a collective benefit", "Measure X would disproportionately restrict liberties"],
        ["A collective benefit", "A disproportionate restriction"],
    ):
        node["en"].update({
            "canonical_title": canonical,
            "displayed_title": displayed,
            "title_status": "locked",
            "sections": ["Society"],
            "keywords": ["measure X"],
        })
    dump(manifest_path, manifest)
    dump(registry_path, registry)
    return manifest, registry


def _insert_link(path: Path, target: str, model: str = "Lien interlangue") -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "|date-création=",
        f"|interlangue={{{{{model}\n|langue=en\n|page={target}\n}}}}\n|date-création=",
    )
    path.write_text(text, encoding="utf-8")


def test_active_english_debate_shape_uses_topic_and_complete_topic():
    spec = TOP[("en", "debate")]
    assert "type" not in spec["order"]
    assert spec["order"][:2] == ["topic", "complete-topic"]
    assert {"topic", "complete-topic"} <= set(spec["required"])


def test_norm_120_requires_direct_french_interlanguage_links(tmp_path: Path):
    root = create_fr_package(tmp_path)
    _activate_120(root)
    report = validate_package(root, scopes=["wikicode"])
    messages = [f.message for f in report.findings if f.code == "WDV-MWK-011"]
    assert len(messages) == 3
    assert all("dès la création" in message for message in messages)


def test_norm_120_uses_lien_interlangue_for_debate_and_arguments(tmp_path: Path):
    root = create_fr_package(tmp_path)
    _, registry = _activate_120(root)
    _insert_link(root / "output/fr/debate/debate.wiki", registry["debate"]["pages"]["en"]["canonical_title"])
    for node in registry["graph"]["nodes"]:
        _insert_link(root / node["pages"]["fr"]["file"]["path"], node["en"]["canonical_title"])
    report = validate_package(root, scopes=["wikicode"])
    assert not any(f.code == "WDV-MWK-011" for f in report.findings), report.to_text()

    debate = root / "output/fr/debate/debate.wiki"
    debate.write_text(debate.read_text(encoding="utf-8").replace("{{Lien interlangue", "{{Interlangue"), encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert any(f.code == "WDV-MWK-011" and "Lien interlangue" in f.message for f in report.findings)


def test_norm_120_rejects_references_tag(tmp_path: Path):
    root = create_fr_package(tmp_path)
    _, registry = _activate_120(root)
    _insert_link(root / "output/fr/debate/debate.wiki", registry["debate"]["pages"]["en"]["canonical_title"])
    p = root / "output/fr/debate/debate.wiki"
    p.write_text(p.read_text(encoding="utf-8").replace("La mesure X est une mesure pilote.", "La mesure X est une mesure pilote.<ref>Source</ref>\n<references />"), encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert any(f.code == "WDV-EDT-010" for f in report.findings), report.to_text()


def test_context_dependent_canonical_titles_are_detected():
    assert contextual_title_issues(
        "La convergence de plusieurs échecs indépendants sur ce protocole réduit sa valeur",
        "fr",
    ) == ["implicit_referent"]
    assert contextual_title_issues(
        "La convergence de plusieurs échecs indépendants sur le protocole de contrôle croisé réduit sa valeur emblématique",
        "fr",
    ) == []
    assert contextual_title_issues(
        "La convergence de plusieurs échecs indépendants réduit la valeur emblématique du protocole de contrôle croisé",
        "fr",
    ) == []


def test_norm_120_prefers_verified_french_equivalent_for_french_argument(tmp_path: Path):
    root = create_graph_package(tmp_path)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    manifest["normative_versions"]["consolidated_norm"] = "1.2.0"
    dump(root / "manifest.json", manifest)
    registry = json.loads((root / "data/registre_debat.json").read_text(encoding="utf-8"))
    registry["graph"]["nodes"][0]["sources"]["fr"]["bibliography"] = ["S00001"]
    dump(root / "data/registre_debat.json", registry)
    sources = {
        "source_registry_version": "1.2",
        "debate_id": "exemple",
        "sources": [
            {
                "id": "S00001", "type": "bibliography", "language": "en", "document_kind": "book",
                "equivalence_group": "work-x",
                "metadata": {"authors": ["A"], "article": None, "work": "Work X", "volume": None, "issue": None, "location": None, "publisher": "P", "place": None, "date": "2020", "link": None, "page": None, "site": None, "title": None},
                "verification": {"status": "verified", "verified_at": "2026-07-23T18:00:00+02:00", "primary_source": True, "notes": [], "language_verified": True, "authorship_checked": True, "authorship_verified": True},
                "usage": [{"page_id": "A0001", "language": "fr", "role": "supports_summary", "language_fit": "original_no_equivalent", "preferred_equivalent_source_id": None, "documentary_scope": "narrow_argument", "selection_reason": "Supports the page."}],
                "deduplication_key": "work-x-en",
            },
            {
                "id": "S00002", "type": "bibliography", "language": "fr", "document_kind": "book",
                "equivalence_group": "work-x",
                "metadata": {"authors": ["A"], "article": None, "work": "Œuvre X", "volume": None, "issue": None, "location": None, "publisher": "P", "place": None, "date": "2020", "link": None, "page": None, "site": None, "title": None},
                "verification": {"status": "verified", "verified_at": "2026-07-23T18:00:00+02:00", "primary_source": True, "notes": [], "language_verified": True, "authorship_checked": True, "authorship_verified": True},
                "usage": [{"page_id": "A0002", "language": "fr", "role": "supports_summary", "language_fit": "native", "preferred_equivalent_source_id": None, "documentary_scope": "narrow_argument", "selection_reason": "Supports another page."}],
                "deduplication_key": "work-x-fr",
            },
        ],
    }
    dump(root / "data/sources.json", sources)
    report = validate_package(root, scopes=["sources"])
    assert any(f.code == "WDV-SRC-004" and "équivalent" in f.message for f in report.findings), report.to_text()


def test_norm_120_rejects_foreign_debate_source_and_narrow_article(tmp_path: Path):
    root = create_graph_package(tmp_path)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    manifest["normative_versions"]["consolidated_norm"] = "1.2.0"
    dump(root / "manifest.json", manifest)
    source = {
        "id": "S00001", "type": "bibliography", "language": "en", "document_kind": "journal_article", "equivalence_group": None,
        "metadata": {"authors": ["A"], "article": "Narrow finding", "work": "Journal", "volume": "1", "issue": "1", "location": None, "publisher": "P", "place": None, "date": "2020", "link": None, "page": "1-5", "site": None, "title": None},
        "verification": {"status": "verified", "verified_at": "2026-07-23T18:00:00+02:00", "primary_source": True, "notes": [], "language_verified": True, "authorship_checked": True, "authorship_verified": True},
        "usage": [{"page_id": "exemple", "language": "fr", "role": "neutral_reference", "language_fit": "original_no_equivalent", "preferred_equivalent_source_id": None, "documentary_scope": "narrow_argument", "selection_reason": "A narrow result only."}],
        "deduplication_key": "narrow",
    }
    dump(root / "data/sources.json", {"source_registry_version": "1.2", "debate_id": "exemple", "sources": [source]})
    report = validate_package(root, scopes=["sources"])
    codes = {f.code for f in report.findings if f.level == "ERROR"}
    assert {"WDV-SRC-004", "WDV-SRC-005"} <= codes, report.to_text()


def test_norm_120_rejects_redundant_web_metadata(tmp_path: Path):
    root = create_graph_package(tmp_path)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    manifest["normative_versions"]["consolidated_norm"] = "1.2.0"
    dump(root / "manifest.json", manifest)
    source = {
        "id": "S00001", "type": "webliography", "language": "fr", "document_kind": None, "equivalence_group": None,
        "metadata": {"authors": ["Organisation X"], "article": None, "work": None, "volume": None, "issue": None, "location": None, "publisher": None, "place": None, "date": None, "link": "https://example.org", "page": "Organisation X", "site": "Organisation X", "title": None},
        "verification": {"status": "verified", "verified_at": "2026-07-23T18:00:00+02:00", "primary_source": True, "notes": [], "language_verified": True, "authorship_checked": True, "authorship_verified": False},
        "usage": [{"page_id": "exemple", "language": "fr", "role": "neutral_reference", "language_fit": "native", "preferred_equivalent_source_id": None, "documentary_scope": "context", "selection_reason": "Contextual institutional page."}],
        "deduplication_key": "web-x",
    }
    dump(root / "data/sources.json", {"source_registry_version": "1.2", "debate_id": "exemple", "sources": [source]})
    report = validate_package(root, scopes=["sources"])
    assert sum(f.code == "WDV-DOC-004" for f in report.findings) >= 2, report.to_text()


def test_explicit_antecedent_with_possessive_is_allowed():
    from wikidebia_validator.graph import contextual_title_issues
    assert contextual_title_issues("Le programme de contrôle croisé a fait approuver son protocole à l'avance", "fr") == []
    assert contextual_title_issues("The cross-check programme had its protocol approved in advance", "en") == []


def test_norm_121_generic_referential_autonomy():
    assert contextual_title_issues("Cette conception affaiblit la cohérence du raisonnement", "fr", "1.2.1") == ["initial_contextual_referent"]
    assert contextual_title_issues("La conception falsificationniste affaiblit la cohérence du raisonnement", "fr", "1.2.1") == []
    assert contextual_title_issues("Le programme de contrôle croisé réduit sa valeur probante après plusieurs échecs", "fr", "1.2.1") == []
    assert contextual_title_issues("Ce que montrent les réplications indépendantes reste contesté", "fr", "1.2.1") == []


def test_norm_121_rejects_parenthetical_em_dashes_in_french_intro(tmp_path: Path):
    root = create_fr_package(tmp_path)
    manifest, registry = _activate_120(root)
    manifest["normative_versions"]["consolidated_norm"] = "1.2.1"
    manifest["normative_versions"]["validator"] = "0.4.1"
    dump(root / "manifest.json", manifest)
    registry["schema"]["validator_version"] = "0.4.1"
    dump(root / "data/registre_debat.json", registry)
    _insert_link(root / "output/fr/debate/debate.wiki", registry["debate"]["pages"]["en"]["canonical_title"])
    p = root / "output/fr/debate/debate.wiki"
    text = p.read_text(encoding="utf-8").replace(
        "La mesure X est une mesure pilote.",
        "La mesure X est une mesure pilote — limitée à deux régions — avant son évaluation.",
    )
    p.write_text(text, encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert any(f.code == "WDV-MWK-015" for f in report.findings), report.to_text()


def test_norm_121_accepts_parentheses_in_french_intro(tmp_path: Path):
    root = create_fr_package(tmp_path)
    manifest, registry = _activate_120(root)
    manifest["normative_versions"]["consolidated_norm"] = "1.2.1"
    manifest["normative_versions"]["validator"] = "0.4.1"
    dump(root / "manifest.json", manifest)
    registry["schema"]["validator_version"] = "0.4.1"
    dump(root / "data/registre_debat.json", registry)
    _insert_link(root / "output/fr/debate/debate.wiki", registry["debate"]["pages"]["en"]["canonical_title"])
    p = root / "output/fr/debate/debate.wiki"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "La mesure X est une mesure pilote.",
        "La mesure X est une mesure pilote (limitée à deux régions) avant son évaluation.",
    ), encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert not any(f.code == "WDV-MWK-015" for f in report.findings), report.to_text()
