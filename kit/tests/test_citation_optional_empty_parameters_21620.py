from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


content = load_module("wikidebia_content_review")
translation = sys.modules.get("wikidebia_translation_review") or load_module("wikidebia_translation_review")
render = sys.modules.get("wikidebia_render") or load_module("wikidebia_render")


def historical_citation(citation_id: str, article: str) -> dict:
    parameters = [
        {"name": "auteurs", "value": "Commission nationale de l'informatique et des libertés (CNIL)"},
        {"name": "article", "value": article},
        {"name": "citation", "value": "Le vote par Internet soulève des questions de sécurité et de confiance dans le scrutin."},
        {"name": "ouvrage", "value": ""},
        {"name": "numéro", "value": ""},
        {"name": "localisation", "value": ""},
        {"name": "page", "value": ""},
        {"name": "édition", "value": ""},
        {"name": "lieu", "value": ""},
        {"name": "date", "value": "28 mai 2006"},
        {"name": "lien", "value": "https://www.cnil.fr/fr/le-vote-par-internet-aux-elections-politiques-les-elements-du-debat"},
    ]
    return {
        "id": citation_id,
        "source_template": "Citation",
        "source_parameters": parameters,
        "citation": next(row["value"] for row in parameters if row["name"] == "citation"),
        "date": "28 mai 2006",
        "avertissements-citation": "",
        "preserved_parameters": [row.copy() for row in parameters if row["name"] not in {"citation", "date", "avertissements-citation"}],
    }


def approved_translation(citation_id: str, source: dict) -> dict:
    return {
        "id": citation_id,
        "source": source,
        "status": "approved",
        "translated_citation": "Internet voting raises questions about security and confidence in the election.",
        "translated_date": "28 May 2006",
        "citation_translated": True,
        "date_translated_or_language_neutral": True,
        "preserved_parameters_unchanged": True,
        "translation_warning_appended": True,
        "quote_completeness_reviewed": True,
        "quote_completeness_note": "The complete quotation was checked against the French source text.",
        "quote_low_ratio_reviewed": True,
        "quote_low_ratio_note": "The translated quotation preserves the complete meaning of the French source.",
        "reviewer": "ChatGPT",
        "reviewed_at": "2026-08-12T22:00:00+02:00",
        "note": "Citation translated and documentary metadata preserved exactly.",
    }


def test_imported_citation_with_optional_empty_parameters_renders_and_omits_only_empty_values():
    source = historical_citation("A0055-C001", "Le vote par Internet aux élections politiques, les éléments du débat")
    wiki = render._citation_template(source, lang="fr")
    assert wiki.startswith("{{Citation\n")
    assert "|citation=Le vote par Internet" in wiki
    assert "|auteurs=Commission nationale" in wiki
    assert "|date=28 mai 2006" in wiki
    assert "|lien=https://" in wiki
    for name in ("ouvrage", "numéro", "localisation", "page", "édition", "lieu"):
        assert f"|{name}=" not in wiki


def test_empty_citation_parameter_name_remains_blocking():
    source = historical_citation("A0055-C001", "Le vote par Internet aux élections politiques, les éléments du débat")
    source["source_parameters"].append({"name": "", "value": "valeur"})
    try:
        render._citation_template(source, lang="fr")
    except render.RenderError as exc:
        assert "Nom de paramètre de citation vide" in str(exc)
    else:
        raise AssertionError("Un nom de paramètre de citation vide a été accepté")


def test_mandatory_citation_value_empty_is_still_rejected_upstream():
    raw = """{{Citation
|auteurs=Commission nationale de l'informatique et des libertés (CNIL)
|article=Le vote par Internet aux élections politiques, les éléments du débat
|citation=
|ouvrage=
|page=
|date=28 mai 2006
|lien=https://example.org/cnil
}}"""
    try:
        content._citation_records(raw, "A0055")
    except content.ContentReviewError as exc:
        assert "sans paramètre citation unique" in str(exc)
    else:
        raise AssertionError("Une Citation dont le paramètre obligatoire citation est vide a été acceptée")


def test_real_vote_electronique_a0055_c001_shape_is_accepted_without_inventing_metadata():
    source = historical_citation("A0055-C001", "Le vote par Internet aux élections politiques, les éléments du débat")
    before = [row.copy() for row in source["source_parameters"]]
    wiki = render._citation_template(source, lang="fr")
    assert source["source_parameters"] == before
    assert "|ouvrage=" not in wiki and "|page=" not in wiki and "|édition=" not in wiki


def test_real_vote_electronique_a0056_c001_shape_is_accepted_without_inventing_metadata():
    source = historical_citation("A0056-C001", "Le vote électronique : quelles garanties pour la démocratie ?")
    before = [row.copy() for row in source["source_parameters"]]
    wiki = render._citation_template(source, lang="fr")
    assert source["source_parameters"] == before
    assert "|numéro=" not in wiki and "|localisation=" not in wiki and "|lieu=" not in wiki


def test_citation_to_quote_preserves_empty_provenance_but_omits_empty_english_parameters():
    source = historical_citation("A0055-C001", "Le vote par Internet aux élections politiques, les éléments du débat")
    final = translation._validate_citations([approved_translation(source["id"], source)], [source], "A0055")[0]

    # Provenance/inventory remains faithful, including historically empty rows.
    assert final["source"] == source
    assert final["source"]["source_parameters"] == source["source_parameters"]
    mapped = {row["name"]: row["value"] for row in final["parameters"]}
    for name in ("work", "issue", "location", "page", "publisher", "place"):
        assert name in mapped and mapped[name] == ""

    wiki = render._citation_template(final, lang="en")
    assert "|quote=Internet voting raises questions" in wiki
    assert "|authors=Commission nationale" in wiki
    assert "|date=28 May 2006" in wiki
    assert "|warnings=AI-translated quote" in wiki
    for name in ("work", "issue", "location", "page", "publisher", "place"):
        assert f"|{name}=" not in wiki

    # No documentary value was invented merely to satisfy the output template.
    assert "Unknown" not in wiki
    assert "N/A" not in wiki
    assert "None" not in wiki
