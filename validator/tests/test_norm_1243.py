from pathlib import Path

from wikidebia_validator.editorial import validate_introduction_review_data


def _entry(*, title: str = "Enjeux du débat", concrete: bool = True):
    stakes = {
        "title": title,
        "purpose": "Présenter les conséquences concrètes des principales réponses possibles.",
        "necessary_for_understanding": True,
        "technical_or_specialized": False,
        "relevance_to_debate_explained": True,
        "stakes_section": True,
        "concrete_stakes": [
            "Une réponse positive modifie le cadre explicatif appliqué au sujet.",
            "Une réponse négative impose d'autres fondements pour les pratiques concernées.",
        ] if concrete else [],
    }
    return {
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
        "information_density_reviewed": True,
        "subsections_non_redundant": True,
        "no_generic_stakes_filler": True,
        "documentation_orientation_reviewed": True,
        "youtube_authorship_reviewed": True,
        "dedicated_stakes_subsection_present": True,
        "stakes_consequences_concrete": True,
        "stakes_not_argument_catalogue": True,
        "complete_topic_fits_heading": True,
        "debate_sections_precise": True,
        "documentation_proportionate_to_literature": True,
        "documentation_family_notes": {
            "bibliography": "La bibliographie couvre les synthèses réellement utiles au débat.",
            "webliography": "La sitographie retient les ressources autonomes réellement informatives.",
            "videography": "La vidéographie retient les contenus substantiels et correctement attribués.",
        },
        "wikipedia_hover_links_reviewed": True,
        "specialized_terms_linked_or_explained": True,
        "common_acronym": None,
        "common_acronym_used_or_not_applicable": True,
        "topic_is_nominal_label": True,
        "conventional_topic_label_used_or_not_applicable": True,
        "complete_topic_lowercase_initial_or_justified": True,
        "topic_label_rationale": "Le libellé nominal est conventionnel, précis et directement compréhensible.",
        "subsections": [
            {
                "title": "Définition",
                "purpose": "Définir le sujet et le périmètre exact du débat.",
                "necessary_for_understanding": True,
                "technical_or_specialized": False,
                "relevance_to_debate_explained": True,
            },
            stakes,
        ],
    }


def _validate(entry, titles=None, content=None):
    titles = titles or ["Définition", entry["subsections"][1]["title"]]
    content = content or (
        "Une réponse positive changerait le cadre explicatif appliqué au sujet et les pratiques qui en dépendent. "
        "Une réponse négative imposerait de rechercher d'autres fondements et d'autres critères de décision. "
        "Une suspension du jugement déplacerait enfin l'attention vers les limites de la preuve et de la connaissance disponible."
    )
    return validate_introduction_review_data(
        {"normative_revision": "1.2.30", "entries": [entry]},
        {"fr": titles},
        norm="1.2.30",
        complete_topics={"fr": "l'exemple"},
        topics={"fr": "Exemple"},
        introduction_policy_revision="1.2.43",
        actual_contents={"fr": {"Définition": "Une définition suffisamment précise.", "Enjeux du débat": content}},
    )


def test_1243_accepts_dedicated_concrete_stakes_subsection():
    issues = _validate(_entry())
    assert not issues


def test_1243_rejects_missing_dedicated_stakes_title():
    entry = _entry(title="Conséquences générales")
    issues = _validate(entry, titles=["Définition", "Conséquences générales"])
    assert any(issue["reason"] == "missing_dedicated_stakes_subsection" for issue in issues)


def test_1243_rejects_stakes_without_two_concrete_consequences():
    issues = _validate(_entry(concrete=False))
    assert any(issue["reason"] == "concrete_stakes_missing" for issue in issues)


def test_1243_rejects_symbolic_stakes_content():
    issues = _validate(_entry(), content="Ce débat comporte des enjeux philosophiques et sociaux.")
    assert any(issue["reason"] == "stakes_subsection_too_thin" for issue in issues)


def test_active_norm_is_1243():
    root = Path(__file__).parents[1] / "normative_reference" / "01_normes"
    assert sorted(p.name for p in root.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md")) == ["WIKIDEBIA_NORME_CONSOLIDEE_1.2.52.md"]
