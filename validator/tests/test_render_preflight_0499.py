from __future__ import annotations

import json
from pathlib import Path
import pytest

from wikidebia_validator.editorial import validate_individual_review_data
from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package


def _historical_nominal_review() -> tuple[dict, list[dict]]:
    nodes = [{
        "id": "A0001",
        "fr": {"canonical_title": "Le vote électronique accélère le décompte", "displayed_title": "Un décompte plus rapide", "rubriques": ["Politique"], "keywords": ["vote électronique"]},
        "en": {"canonical_title": "Electronic voting speeds up counting", "displayed_title": "Faster vote counting", "sections": ["Politics"], "keywords": ["electronic voting"]},
    }]
    review = {"entries": [{
        "id": "A0001",
        "title_decision": "retained_after_review",
        "title_reason": "Historical displayed title retained after explicit metadata review and translated without semantic degradation.",
        "canonical_referents_explicit_fr": True,
        "canonical_referents_explicit_en": True,
        "canonical_title_semantic_inventory_reviewed_en": True,
        "canonical_title_semantic_inventory_note_en": "Subject, predicate, scope and modality were checked against the French canonical title.",
        "canonical_title_semantically_equivalent_en": True,
        "canonical_title_subject_preserved_en": True,
        "canonical_title_predicate_preserved_en": True,
        "canonical_title_scope_preserved_en": True,
        "canonical_title_modality_preserved_en": True,
        "displayed_referents_explicit_fr": None,
        "displayed_referents_explicit_en": None,
        "displayed_title_complete_proposition_fr": False,
        "displayed_title_argument_intelligible_fr": True,
        "displayed_title_source_form_reviewed_fr": True,
        "displayed_title_source_form_fr": "nominal_phrase",
        "displayed_title_complete_proposition_en": False,
        "displayed_title_argument_intelligible_en": True,
        "displayed_title_source_form_reviewed_en": True,
        "displayed_title_no_formal_regression_en": True,
        "displayed_title_semantic_inventory_reviewed_en": True,
        "displayed_title_source_form_en": "nominal_phrase",
        "displayed_title_target_form_en": "nominal_phrase",
        "displayed_title_semantic_inventory_note_en": "The historical nominal displayed-title form is preserved without semantic degradation.",
        "displayed_title_subject_preserved_en": True,
        "displayed_title_predicate_preserved_en": True,
        "displayed_title_scope_preserved_en": True,
        "displayed_title_modality_preserved_en": True,
        "displayed_title_concision_reviewed_fr": True,
        "displayed_title_concision_reviewed_en": True,
        "displayed_title_semantically_equivalent_fr": True,
        "displayed_title_semantically_equivalent_en": True,
        "displayed_title_semantic_equivalence_reviewed_fr": True,
        "displayed_title_semantic_equivalence_reviewed_en": True,
        "displayed_title_readability_improvement_reviewed_fr": True,
        "displayed_title_readability_improvement_reviewed_en": True,
        "new_displayed_title_fr": "Un décompte plus rapide",
        "new_displayed_title_en": "Faster vote counting",
        "new_rubriques": ["Politique"],
        "new_sections_en": ["Politics"],
        "new_keywords_fr": ["vote électronique"],
        "new_keywords_en": ["electronic voting"],
        "keywords_ordered_by_relevance_fr": True,
        "keywords_ordered_by_relevance_en": True,
        "keyword_order_rationale_fr": "Le concept le plus directement pertinent est classé en premier.",
        "keyword_order_rationale_en": "The most directly relevant concept remains first in the English order.",
        "rubric_decision": "retained_after_review",
        "rubric_rationales": {"Politique": "Le raisonnement porte directement sur l'organisation du scrutin."},
    }]}
    return review, nodes


def test_historical_nominal_displayed_title_does_not_require_english_creation_profile():
    review, nodes = _historical_nominal_review()
    issues = validate_individual_review_data(
        review,
        nodes,
        english_deferred=False,
        displayed_title_policy_node_ids=set(),
        translation_validation_mode="differential",
        translation_semantic_review_schema_version="1.4",
        preexisting_node_ids={"A0001"},
    )
    assert not any(issue.get("reason") == "displayed_title_complete_proposition_en" for issue in issues), issues


def test_translation_does_not_require_generation_readability_or_autonomy_attestations():
    review, nodes = _historical_nominal_review()
    entry = review["entries"][0]
    entry.update(displayed_title_readability_improvement_reviewed_fr=False,
                 displayed_title_readability_improvement_reviewed_en=False,
                 displayed_referents_explicit_fr=False, displayed_referents_explicit_en=False,
                 title_reason="Source form preserved.")
    issues = validate_individual_review_data(review, nodes, translation_validation_mode="differential",
        translation_semantic_review_schema_version="1.4", displayed_title_policy_node_ids={"A0001"})
    generation_reasons = {"displayed_referents_explicit", "displayed_title_difference_reason",
        "displayed_title_readability_improvement_reviewed_fr", "displayed_title_readability_improvement_reviewed_en"}
    assert not any(issue.get("reason") in generation_reasons for issue in issues), issues


@pytest.mark.parametrize("mode", ("absolute", "differential"))
@pytest.mark.parametrize("fr,en", [("Coûts", "Costs"),
    ("Des coûts supplémentaires pour les contribuables et pour les entreprises de chaque région",
     "Additional costs for taxpayers and for businesses in every region of the country")])
def test_displayed_title_length_and_form_are_generation_rules(tmp_path: Path, mode, fr, en):
    create_fr_package(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest.setdefault("editorial_controls", {})["translation_validation_mode"] = mode
    manifest_path.write_text(json.dumps(manifest))
    registry_path = tmp_path / "data/registre_debat.json"
    registry = json.loads(registry_path.read_text())
    registry["graph"]["nodes"][0]["fr"]["displayed_title"] = fr
    registry["graph"]["nodes"][0]["en"]["displayed_title"] = en
    registry_path.write_text(json.dumps(registry))
    report = validate_package(tmp_path, scopes=["editorial"])
    form_errors = [f for f in report.findings if f.level == "ERROR" and f.code in {"WDV-EDT-007", "WDV-EDT-021", "WDV-EDT-001"}
                   and f.details.get("node_id") == "A0001"]
    if mode == "absolute":
        assert form_errors, report.to_text()
    else:
        assert not form_errors, report.to_text()


def test_inline_machine_date_scanner_ignores_iso_like_url_but_blocks_prose_date(tmp_path: Path):
    create_fr_package(tmp_path)
    debate = tmp_path / "output/fr/debate/debate.wiki"
    text = debate.read_text(encoding="utf-8")
    text = text.replace(
        "|contenu=La mesure X est une mesure pilote.",
        "|contenu=La mesure X est une mesure pilote<ref>Institution, rapport, https://example.org/archive/2024-07-09/report</ref>.",
        1,
    )
    debate.write_text(text, encoding="utf-8")
    report = validate_package(tmp_path, scopes=["editorial"])
    assert not any(f.level == "ERROR" and f.code == "WDV-DOC-005" for f in report.findings), report.to_text()

    text = debate.read_text(encoding="utf-8").replace(
        "Institution, rapport, https://example.org/archive/2024-07-09/report",
        "Institution, rapport, 2024-07-09, https://example.org/archive/2024-07-09/report",
        1,
    )
    debate.write_text(text, encoding="utf-8")
    report = validate_package(tmp_path, scopes=["editorial"])
    assert any(f.level == "ERROR" and f.code == "WDV-DOC-005" for f in report.findings), report.to_text()
