from pathlib import Path

from wikidebia_validator.editorial import validate_introduction_review_data


def _review():
    return {
        "review_version": "1.0",
        "normative_revision": "1.2.4",
        "debate_id": "exemple",
        "entries": [
            {
                "language": "fr",
                "subject_and_scope_defined": True,
                "debate_question_explained": True,
                "history_and_evolution_addressed": True,
                "current_state_addressed_or_not_applicable": True,
                "stakes_explained": True,
                "factual_claims_referenced": True,
                "progression_coherent": True,
                "no_argument_tree_mirroring": True,
                "no_topic_specific_checklist": True,
                "subsections": [
                    {
                        "title": "Définition et périmètre",
                        "purpose": "Définir le sujet et ses limites.",
                        "necessary_for_understanding": True,
                        "technical_or_specialized": False,
                        "relevance_to_debate_explained": True,
                    },
                    {
                        "title": "Enjeux du débat",
                        "purpose": "Expliquer pourquoi la réponse importe.",
                        "necessary_for_understanding": True,
                        "technical_or_specialized": False,
                        "relevance_to_debate_explained": True,
                    },
                ],
            },
            {
                "language": "en",
                "subject_and_scope_defined": True,
                "debate_question_explained": True,
                "history_and_evolution_addressed": True,
                "current_state_addressed_or_not_applicable": True,
                "stakes_explained": True,
                "factual_claims_referenced": True,
                "progression_coherent": True,
                "no_argument_tree_mirroring": True,
                "no_topic_specific_checklist": True,
                "subsections": [
                    {
                        "title": "Definition and scope",
                        "purpose": "Define the subject and its boundaries.",
                        "necessary_for_understanding": True,
                        "technical_or_specialized": False,
                        "relevance_to_debate_explained": True,
                    },
                    {
                        "title": "Stakes of the debate",
                        "purpose": "Explain why the answer matters.",
                        "necessary_for_understanding": True,
                        "technical_or_specialized": False,
                        "relevance_to_debate_explained": True,
                    },
                ],
            },
        ],
    }


def test_norm_124_accepts_complete_bilingual_introduction_review():
    actual = {
        "fr": ["Définition et périmètre", "Enjeux du débat"],
        "en": ["Definition and scope", "Stakes of the debate"],
    }
    assert validate_introduction_review_data(_review(), actual, norm="1.2.4") == []


def test_norm_124_rejects_missing_stakes_and_title_mismatch():
    review = _review()
    review["entries"][0]["stakes_explained"] = False
    review["entries"][0]["subsections"][1]["title"] = "Section technique"
    actual = {
        "fr": ["Définition et périmètre", "Enjeux du débat"],
        "en": ["Definition and scope", "Stakes of the debate"],
    }
    reasons = {issue["reason"] for issue in validate_introduction_review_data(review, actual, norm="1.2.4")}
    assert "attestation_false_or_missing" in reasons
    assert "subsection_titles_mismatch" in reasons


def test_norm_124_rejects_unexplained_technical_subsection():
    review = _review()
    row = review["entries"][0]["subsections"][1]
    row["technical_or_specialized"] = True
    row["relevance_to_debate_explained"] = False
    actual = {
        "fr": ["Définition et périmètre", "Enjeux du débat"],
        "en": ["Definition and scope", "Stakes of the debate"],
    }
    reasons = {issue["reason"] for issue in validate_introduction_review_data(review, actual, norm="1.2.4")}
    assert "technical_relevance_not_explained" in reasons


def test_norm_124_active_rules_are_corpus_generic():
    root = Path(__file__).parents[1] / "normative_reference" / "01_normes"
    active_files = [
        root / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.28.md",
        root / "profils_rendu_wikidebia.md",
        root / "workflow_production_wikidebia.md",
        root / "schema_graphe_registre_wikidebia.md",
        root / "cahier_des_charges_consolide_wikidebia.md",
    ]
    forbidden = (
        "parapsychologie",
        "transparent psi",
        "ganzfeld",
        "reseaux_sociaux_adolescents",
        "réseaux sociaux aux adolescents",
    )
    combined = "\n".join(path.read_text(encoding="utf-8").casefold() for path in active_files)
    assert all(token not in combined for token in forbidden)
