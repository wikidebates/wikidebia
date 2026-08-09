from pathlib import Path

from .current_policy_helpers import complete_summary_decision

from wikidebia_validator.editorial import (
    opening_title_similarity,
    summary_quantitative_claims,
    validate_summary_style_review_data,
)


def _decision(**overrides):
    value = {
        "status": "revised",
        "thesis_first": True,
        "general_public_style": True,
        "sentence_rhythm_reviewed": True,
        "technical_terms_reviewed": True,
        "opening_develops_title": True,
        "example_or_data_reviewed": True,
        "assertive_tone_reviewed": True,
        "no_artificial_example_or_number": True,
        "no_polemical_overstatement": True,
        "note": "Résumé relu page par page selon les exigences de la norme 1.1.9.",
    }
    value.update(overrides)
    completed, _ = complete_summary_decision(value)
    return completed


def test_exact_title_repetition_triggers_opening_warning():
    title = "La comparaison sociale répétée peut dégrader l'estime de soi"
    summary = title + ". Elle impose ensuite des classements visibles."
    assert opening_title_similarity(summary, [title], "fr")["issue"] is True


def test_developed_opening_does_not_trigger_title_warning():
    title = "La comparaison sociale répétée peut dégrader l'estime de soi"
    summary = "Sur un fil d'actualité, la vie ordinaire se mesure à une succession de réussites soigneusement sélectionnées. Cette comparaison faussée peut diminuer l'estime de soi."
    assert opening_title_similarity(summary, [title], "fr")["issue"] is False


def test_close_paraphrase_with_only_small_addition_triggers():
    title = "Les notifications nocturnes peuvent perturber le sommeil"
    summary = "Les notifications nocturnes peuvent perturber le sommeil. Elles retardent le coucher."
    assert opening_title_similarity(summary, [title], "fr")["issue"] is True


def test_quantitative_claim_detector_ignores_reference_body():
    claims = summary_quantitative_claims("Une enquête de 2024 porte sur 1 250 personnes et observe 25 %. <ref>Étude 2020, p. 12</ref>")
    assert "2024" in claims
    assert "25 %" in claims
    assert "2020" not in claims
    assert "12" not in claims


def test_119_review_requires_new_human_attestations():
    review = {
        "normative_revision": "1.1.9",
        "entries": [{"id": "A0001", "languages": {"fr": _decision()}}],
    }
    assert validate_summary_style_review_data(review, [{"id": "A0001"}], {"A0001": {"fr"}}, norm="1.1.9", summaries={("A0001", "fr"): complete_summary_decision()[1]}) == []
    review["entries"][0]["languages"]["fr"]["opening_develops_title"] = False
    issues = validate_summary_style_review_data(review, [{"id": "A0001"}], {"A0001": {"fr"}}, norm="1.1.9", summaries={("A0001", "fr"): complete_summary_decision()[1]})
    assert any(i["reason"] == "opening_develops_title" for i in issues)


def test_quantitative_summary_requires_explicit_verification():
    review = {
        "normative_revision": "1.1.9",
        "entries": [{"id": "A0001", "languages": {"fr": _decision()}}],
    }
    issues = validate_summary_style_review_data(
        review,
        [{"id": "A0001"}],
        {"A0001": {"fr"}},
        norm="1.1.9",
        quantitative_pages={("A0001", "fr")},
        summaries={("A0001", "fr"): complete_summary_decision()[1]},
    )
    assert any(i["reason"] == "quantitative_claims_verified" for i in issues)
    assert any(i["reason"] == "quantitative_claims_note" for i in issues)
    decision = review["entries"][0]["languages"]["fr"]
    decision["quantitative_claims_verified"] = True
    decision["quantitative_claims_note"] = "Population, période, contexte et source documentaire ont été vérifiés."
    assert validate_summary_style_review_data(
        review,
        [{"id": "A0001"}],
        {"A0001": {"fr"}},
        norm="1.1.9",
        quantitative_pages={("A0001", "fr")},
        summaries={("A0001", "fr"): complete_summary_decision()[1]},
    ) == []


def test_old_norm_metadata_does_not_disable_current_summary_rules():
    review = {
        "entries": [{
            "id": "A0001",
            "languages": {"fr": {
                "status": "approved",
                "thesis_first": True,
                "general_public_style": True,
                "sentence_rhythm_reviewed": True,
                "technical_terms_reviewed": True,
                "note": "Ancienne métadonnée de norme, sans effet sur les règles courantes.",
            }},
        }],
    }
    issues = validate_summary_style_review_data(review, [{"id": "A0001"}], {"A0001": {"fr"}}, norm="1.1.8", summaries={("A0001", "fr"): complete_summary_decision()[1]})
    assert any(i["reason"] == "opening_develops_title" for i in issues)
    assert any(i["reason"] == "originality_reviewed" for i in issues)


def test_active_norm_is_119():
    root = Path(__file__).parents[1] / "normative_reference" / "01_normes"
    assert sorted(p.name for p in root.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md")) == ["WIKIDEBIA_NORME_CONSOLIDEE_1.2.57.md"]
