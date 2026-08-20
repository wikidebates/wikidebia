from __future__ import annotations

from wikidebia_validator.editorial import (
    keyword_form_issues,
    validate_introduction_review_data,
)


def test_long_keyword_is_allowed_when_controlled_multiword_exception_is_already_valid():
    phrase = "réduction du temps de travail"
    assert keyword_form_issues([phrase, "travail"], allowed_long_keywords={phrase}) == []


def test_long_keyword_without_controlled_exception_remains_blocked():
    phrase = "réduction du temps de travail"
    assert "too_many_words" in keyword_form_issues([phrase, "travail"])


def test_preserved_historical_intro_does_not_reactivate_stale_proposed_subsections():
    review = {
        "entries": [{
            "language": "fr",
            "status": "historical_existing",
            "historical_content_preserved": True,
            "historical_source_sha256": "a" * 64,
            "note": "Introduction historique préservée exactement.",
            "subsections": [{"title": "Ancienne proposition non retenue"}],
            "specialized_term_inventory": [{"subsection_title": "Ancienne proposition non retenue"}],
        }]
    }
    issues = validate_introduction_review_data(
        review,
        {"fr": ["Titre historique 1", "Titre historique 2"]},
        complete_topics={"fr": "le test"},
        topics={"fr": "Test"},
    )
    assert not any(i["reason"] in {"subsection_titles_mismatch", "missing_dedicated_stakes_subsection", "specialized_term_inventory_subsections_mismatch"} for i in issues), issues


def test_authorized_historical_intro_still_has_to_match_selected_final_structure():
    review = {
        "entries": [{
            "language": "fr",
            "status": "historical_authorized_change",
            "owner_authorized_change": True,
            "authorization": {"scope": "introduction"},
            "historical_source_sha256": "a" * 64,
            "authorized_final_sha256": "b" * 64,
            "note": "Modification historique explicitement autorisée.",
            "subsections": [{"title": "Mauvais titre"}],
        }]
    }
    issues = validate_introduction_review_data(
        review,
        {"fr": ["Titre final"]},
        complete_topics={"fr": "le test"},
        topics={"fr": "Test"},
    )
    assert any(i["reason"] == "subsection_titles_mismatch" for i in issues), issues


def _historical_en_review(family_notes):
    return {
        "entries": [{
            "language": "en",
            "source_page_origin": "preexisting",
            "historical_source_profile_respected": True,
            "france_specific_context_reviewed": True,
            "international_context_adaptation_reviewed": True,
            "no_unjustified_substantive_addition": True,
            "english_documentation_localized": True,
            "canonical_title_semantic_inventory_reviewed": True,
            "canonical_title_semantic_inventory_note": "Canonical title meaning and scope were reviewed against the source.",
            "topic_semantic_equivalence_reviewed": True,
            "complete_topic_semantic_equivalence_reviewed": True,
            "introduction_claim_inventory_reviewed": True,
            "introduction_claim_inventory_note": "All material claims and historical boundaries were reviewed against the French source.",
            "subsection_structure_equivalence_reviewed": True,
            "factual_claims_referenced": True,
            "documentation_proportionate_to_literature": True,
            "wikipedia_hover_links_reviewed": True,
            "specialized_terms_linked_or_explained": True,
            "documentation_orientation_reviewed": True,
            "youtube_authorship_reviewed": True,
            "reference_note_punctuation_reviewed": True,
            "specialized_term_inventory_reviewed": True,
            "introduction_adaptation_rationale": "The historical source was adapted for English readers without changing the question or scope.",
            "documentation_family_notes": family_notes,
            "subsections": [{"title": "History"}],
            "specialized_term_inventory": [],
        }]
    }


def test_historical_translation_accepts_orientation_specific_documentation_family_notes():
    notes = {
        "pro-bibliography": "Reviewed affirmative bibliography and retained only relevant sources.",
        "con-bibliography": "Reviewed negative bibliography and retained only relevant sources.",
        "bibliography": "Reviewed neutral bibliography and retained only relevant sources.",
        "pro-webliography": "Reviewed affirmative web sources and retained only relevant sources.",
        "con-webliography": "Reviewed negative web sources and retained only relevant sources.",
        "webliography": "Reviewed neutral web sources and retained only relevant sources.",
        "pro-videography": "Reviewed affirmative video sources and retained only relevant sources.",
        "con-videography": "Reviewed negative video sources and retained only relevant sources.",
        "videography": "Reviewed neutral video sources and retained only relevant sources.",
    }
    issues = validate_introduction_review_data(
        _historical_en_review(notes),
        {"en": ["History"]},
        complete_topics={"en": "the test"},
        topics={"en": "Test"},
    )
    assert not any(i["reason"] == "documentation_family_notes" for i in issues), issues


def test_historical_translation_rejects_incomplete_documentation_family_note_shape():
    issues = validate_introduction_review_data(
        _historical_en_review({"bibliography": "Reviewed bibliography in sufficient detail for this test."}),
        {"en": ["History"]},
        complete_topics={"en": "the test"},
        topics={"en": "Test"},
    )
    assert any(i["reason"] == "documentation_family_notes" for i in issues), issues
