from wikidebia_validator.editorial import validate_individual_review_data, validate_introduction_review_data
from wikidebia_validator.report import Report


def _node():
    return {
        "id": "A0001", "status": "active",
        "fr": {"canonical_title": "Dieu existe car une raison l'établit", "displayed_title": "Une raison établit que Dieu existe", "rubriques": [], "keywords": []},
        "en": {"canonical_title": "God exists because a reason establishes it", "displayed_title": "A reason establishes that God exists", "sections": [], "keywords": []},
    }


def _entry():
    return {
        "id": "A0001", "title_decision": "reformulated", "title_reason": "The translated title was reviewed against the authoritative French source in full.",
        "canonical_referents_explicit_fr": True, "canonical_referents_explicit_en": True,
        "displayed_referents_explicit_fr": True, "displayed_referents_explicit_en": True,
        "displayed_title_argument_intelligible_fr": True, "displayed_title_argument_intelligible_en": True,
        "displayed_title_source_form_reviewed_fr": True, "displayed_title_source_form_reviewed_en": True,
        "displayed_title_no_formal_regression_en": True, "displayed_title_semantic_inventory_reviewed_en": True,
        "displayed_title_source_form_fr": "proposition", "displayed_title_source_form_en": "proposition", "displayed_title_target_form_en": "proposition",
        "displayed_title_complete_proposition_en": True,
        "displayed_title_semantic_inventory_note_en": "Subject, predicate, polarity, modality, attribution, quantifiers and logical scope were compared.",
        "displayed_title_concision_reviewed_fr": True, "displayed_title_concision_reviewed_en": True,
        "displayed_title_semantic_equivalence_reviewed_fr": True, "displayed_title_semantic_equivalence_reviewed_en": True,
        "displayed_title_readability_improvement_reviewed_fr": True, "displayed_title_readability_improvement_reviewed_en": True,
        "new_displayed_title_fr": "Une raison établit que Dieu existe", "new_displayed_title_en": "A reason establishes that God exists",
        "new_rubriques": [], "new_sections_en": [], "new_keywords_fr": [], "new_keywords_en": [],
        "keywords_ordered_by_relevance_fr": True, "keywords_ordered_by_relevance_en": True,
        "keyword_order_rationale_fr": "No keywords in this fixture.", "keyword_order_rationale_en": "No keywords in this fixture.",
        "rubric_decision": "retained_after_review", "rubric_rationales": {},
    }


def test_1257_requires_canonical_title_semantic_inventory_in_differential_translation():
    issues = validate_individual_review_data({"entries": [_entry()]}, [_node()], norm="1.2.57", translation_validation_mode="differential", translation_semantic_review_schema_version="1.1")
    reasons = {i["reason"] for i in issues}
    assert "canonical_title_semantic_inventory_reviewed_en" in reasons
    assert "canonical_title_semantically_equivalent_en" in reasons
    assert "canonical_title_semantic_inventory_note_en" in reasons


def test_1256_does_not_retroactively_require_1257_canonical_fields():
    issues = validate_individual_review_data({"entries": [_entry()]}, [_node()], norm="1.2.56", translation_validation_mode="differential", translation_semantic_review_schema_version="1.0")
    reasons = {i["reason"] for i in issues}
    assert "canonical_title_semantic_inventory_reviewed_en" not in reasons
    assert "canonical_title_semantically_equivalent_en" not in reasons
    assert "canonical_title_semantic_inventory_note_en" not in reasons


def _intro_entry(lang):
    return {"language": lang, "subsections": []}


def test_1257_requires_debate_semantic_inventory_for_english_translation():
    review = {"entries": [_intro_entry("fr"), _intro_entry("en")]}
    issues = validate_introduction_review_data(review, {"fr": [], "en": []}, norm="1.2.57", complete_topics={"fr": "x", "en": "x"}, topics={"fr": "X", "en": "X"}, translation_semantic_review_schema_version="1.1")
    en_reasons = {(i.get("reason"), i.get("field")) for i in issues if i.get("language") == "en"}
    assert ("attestation_false_or_missing", "introduction_claim_inventory_reviewed") in en_reasons
    assert any(i.get("reason") == "canonical_title_semantic_inventory_note" and i.get("language") == "en" for i in issues)
    assert any(i.get("reason") == "introduction_claim_inventory_note" and i.get("language") == "en" for i in issues)


def test_report_explicitly_scopes_passed_as_automated_validation():
    report = Report("0.4.60", "package", ["all"])
    payload = report.to_dict()
    assert payload["result"] == "passed"
    assert payload["result_scope"] == "automated_validation"
    assert "human review" in payload["result_meaning"]
    assert "VALIDATION AUTOMATISÉE GLOBALE" in report.to_text()
