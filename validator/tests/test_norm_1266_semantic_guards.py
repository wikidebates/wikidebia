from wikidebia_validator.editorial import (
    bilingual_semantic_marker_losses,
    bilingual_semantic_structure_signals,
    displayed_title_argument_issues,
)


def test_english_displayed_title_requires_main_clause_predicate():
    assert "missing_explicit_predicate" in displayed_title_argument_issues(
        "Highly improbable events that shape history", "en"
    )
    assert "missing_explicit_predicate" in displayed_title_argument_issues(
        "Evidence that challenges the theory", "en"
    )
    assert not displayed_title_argument_issues(
        "Evidence that challenges the theory is weak", "en"
    )
    assert not displayed_title_argument_issues(
        "Those who believe the claim are mistaken", "en"
    )


def test_semantic_marker_engine_covers_hypothesis_force_and_several_scope():
    losses = bilingual_semantic_marker_losses(
        "Plusieurs observations démontrent que l'hypothèse de la réincarnation est nécessaire",
        "Observations support reincarnation",
    )
    assert "several_quantifier" in losses
    assert "strong_probative_force" in losses
    assert "hypothesis_status" in losses
    assert "necessity" in losses


def test_structured_semantic_risks_cover_real_translation_failures():
    signals = bilingual_semantic_structure_signals(
        "Puisque plusieurs cultures interprètent ce phénomène comme une manifestation, cela prouve que l'existence de la vie sur Terre est singulière.",
        "If a culture sees the phenomenon as a sign, this supports the origin of life.",
    )
    assert "interpretation_status_lost" in signals
    assert "probative_force_weakened" in signals
    assert "plural_or_several_scope_lost" in signals
    assert "causal_relation_shifted_to_condition" in signals
    assert "earth_scope_anchor_lost" in signals
    assert "life_existence_shifted_to_origin" in signals


def test_generic_deity_detector_does_not_misclassify_de_Dieu():
    signals = bilingual_semantic_structure_signals(
        "L'hypothèse de Dieu est discutée.",
        "The hypothesis of God is debated.",
    )
    assert "generic_deity_to_proper_God" not in signals


def test_lexical_risk_pairs_are_review_signals():
    signals = bilingual_semantic_structure_signals(
        "La diversité religieuse agit intrinsèquement et collectivement sur les conditions de vie.",
        "Religion affects society.",
    )
    assert "religious_diversity_qualifier_lost" in signals
    assert "inherent_qualifier_lost" in signals
    assert "collective_scope_lost" in signals
    assert "living_conditions_qualifier_lost" in signals
