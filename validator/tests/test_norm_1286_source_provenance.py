from __future__ import annotations

from wikidebia_validator.editorial import (
    INTRO_REVIEW_TRUE_FIELDS,
    keyword_form_issues,
    validate_introduction_review_data,
)


def test_historical_keywords_keep_intrinsic_quality_checks_without_creation_quota():
    keywords = [
        "revenu de base",
        "redistribution",
        "travail",
        "pauvreté",
        "mot-clé historique beaucoup trop long pour être un concept de navigation canonique",
    ]
    issues = keyword_form_issues(keywords, enforce_count=False)
    assert "count" not in issues
    assert "too_long" in issues
    assert "too_many_words" in issues


def _historical_en_intro_entry():
    return {
        "language": "en",
        "source_page_origin": "preexisting",
        "historical_source_profile_respected": True,
        "france_specific_context_reviewed": True,
        "international_context_adaptation_reviewed": True,
        "no_unjustified_substantive_addition": True,
        "english_documentation_localized": True,
        "factual_claims_referenced": True,
        "documentation_proportionate_to_literature": True,
        "wikipedia_hover_links_reviewed": True,
        "specialized_terms_linked_or_explained": True,
        "documentation_orientation_reviewed": True,
        "youtube_authorship_reviewed": True,
        "reference_note_punctuation_reviewed": True,
        "specialized_term_inventory_reviewed": True,
        "introduction_adaptation_rationale": "France-specific institutional details were reviewed and only the context useful to an international reader was retained without changing the debate's substance.",
        "canonical_title_semantic_inventory_reviewed": True,
        "canonical_title_semantic_inventory_note": "Subject, predicate, modality and scope were checked against the French source.",
        "topic_semantic_equivalence_reviewed": True,
        "complete_topic_semantic_equivalence_reviewed": True,
        "introduction_claim_inventory_reviewed": True,
        "introduction_claim_inventory_note": "All substantive claims and distinctions retained in the localized English introduction were checked against the authoritative French source.",
        "subsection_structure_equivalence_reviewed": True,
        "documentation_family_notes": {
            "bibliography": "English-language references were reviewed for the historical introduction.",
            "webliography": "English-language web references were reviewed for the historical introduction.",
            "videography": "English-language video references were reviewed for the historical introduction.",
        },
        "subsections": [{"title": "Definition and history"}],
        "specialized_term_inventory": [],
    }


def test_historical_english_introduction_does_not_require_stakes_subsection():
    issues = validate_introduction_review_data(
        {"entries": [_historical_en_intro_entry()]},
        {"en": ["Definition and history"]},
        actual_contents={"en": {"Definition and history": "Historical context."}},
        translation_semantic_review_schema_version="1.4",
    )
    assert not any(issue.get("reason") == "missing_dedicated_stakes_subsection" for issue in issues)
    assert issues == []


def test_new_english_introduction_still_requires_creation_profile_stakes():
    entry = _historical_en_intro_entry()
    entry.pop("source_page_origin")
    for key in list(entry):
        if key.startswith("historical_") or key in {
            "france_specific_context_reviewed",
            "international_context_adaptation_reviewed",
            "no_unjustified_substantive_addition",
            "english_documentation_localized",
            "introduction_adaptation_rationale",
        }:
            entry.pop(key, None)
    for field in INTRO_REVIEW_TRUE_FIELDS:
        entry[field] = True
    for field in (
        "information_density_reviewed", "subsections_non_redundant", "no_generic_stakes_filler",
        "documentation_orientation_reviewed", "youtube_authorship_reviewed", "dedicated_stakes_subsection_present",
        "stakes_consequences_concrete", "stakes_not_argument_catalogue", "complete_topic_fits_heading",
        "debate_sections_precise", "documentation_proportionate_to_literature", "wikipedia_hover_links_reviewed",
        "specialized_terms_linked_or_explained", "common_acronym_used_or_not_applicable", "topic_is_nominal_label",
        "conventional_topic_label_used_or_not_applicable", "complete_topic_lowercase_initial_or_justified",
        "reference_note_punctuation_reviewed", "specialized_term_inventory_reviewed",
    ):
        entry[field] = True
    entry.update({
        "topic_label_rationale": "A clear nominal topic label is used.",
        "common_acronym": None,
        "terminal_period_sentence_exceptions": [],
    })
    issues = validate_introduction_review_data(
        {"entries": [entry]},
        {"en": ["Definition and history"]},
        complete_topics={"en": "the question under debate"},
        topics={"en": "Basic income"},
        actual_contents={"en": {"Definition and history": "Historical context."}},
        translation_semantic_review_schema_version="1.4",
    )
    assert any(issue.get("reason") == "missing_dedicated_stakes_subsection" for issue in issues)
