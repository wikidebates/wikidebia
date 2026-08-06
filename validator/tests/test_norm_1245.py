from pathlib import Path
from wikidebia_validator.editorial import validate_introduction_review_data


def _review(linked=True):
    terms = [
        {"term": "théisme", "article": "théisme", "linked": True},
        {"term": "déisme", "article": "déisme", "linked": linked},
        {"term": "panthéisme", "article": "panthéisme", "linked": True},
    ]
    if not linked:
        terms[1]["justification"] = "Le terme est défini intégralement dans le passage et ne nécessite pas de survol."
    entry = {
        "language":"fr",
        "subject_and_scope_defined":True,"debate_question_explained":True,"history_and_evolution_addressed":True,
        "current_state_addressed_or_not_applicable":True,"stakes_explained":True,"factual_claims_referenced":True,
        "progression_coherent":True,"no_argument_tree_mirroring":True,"no_topic_specific_checklist":True,
        "complete_topic_fits_heading":True,"debate_sections_precise":True,"documentation_proportionate_to_literature":True,
        "documentation_family_notes":{"bibliography":"Une sélection bibliographique suffisamment détaillée.","webliography":"Une sélection sitographique suffisamment détaillée.","videography":"Une sélection vidéographique suffisamment détaillée."},
        "wikipedia_hover_links_reviewed":True,"specialized_terms_linked_or_explained":True,
        "common_acronym":None,"common_acronym_used_or_not_applicable":True,"topic_is_nominal_label":True,
        "conventional_topic_label_used_or_not_applicable":True,"complete_topic_lowercase_initial_or_justified":True,
        "topic_label_rationale":"Le sujet est formulé sous une forme nominale conventionnelle.",
        "subsections":[{"title":"Conceptions","purpose":"Distinguer plusieurs conceptions du divin.","necessary_for_understanding":True,"technical_or_specialized":True,"relevance_to_debate_explained":True}],
        "wikipedia_link_consistency_reviewed":True,
        "wikipedia_link_groups":[{"subsection_title":"Conceptions","rationale":"Ces doctrines sont coordonnées et présentent le même besoin explicatif.","terms":terms}],
    }
    return {"schema_version":"1.0","normative_revision":"1.2.45","entries":[entry]}


def _issues(review, content):
    return validate_introduction_review_data(review,{"fr":["Conceptions"]},norm="1.2.45",complete_topics={"fr":"l’existence de Dieu"},topics={"fr":"Dieu"},wikipedia_link_consistency_policy_revision="1.2.45",actual_contents={"fr":{"Conceptions":content}})


def test_1245_accepts_uniform_links():
    content="Le {{Lien Wikipédia|article=théisme}}, le {{Lien Wikipédia|article=déisme}} et le {{Lien Wikipédia|article=panthéisme}} sont distingués."
    assert not [i for i in _issues(_review(),content) if i["reason"].startswith("wikipedia") or i["reason"]=="declared_wikipedia_link_missing"]


def test_1245_rejects_declared_link_missing_from_subsection():
    content="Le {{Lien Wikipédia|article=théisme}}, le déisme et le {{Lien Wikipédia|article=panthéisme}} sont distingués."
    assert any(i["reason"]=="declared_wikipedia_link_missing" for i in _issues(_review(),content))


def test_1245_accepts_explicitly_justified_exception():
    content="Le {{Lien Wikipédia|article=théisme}}, le déisme et le {{Lien Wikipédia|article=panthéisme}} sont distingués."
    assert not any(i["reason"] in {"declared_wikipedia_link_missing","unlinked_peer_term_unjustified"} for i in _issues(_review(False),content))


def test_norm_1245_is_preserved_in_history():
    root=Path(__file__).parents[1]/"normative_reference"/"01_normes"
    assert (root / "history/WIKIDEBIA_NORME_CONSOLIDEE_1.2.45.md").is_file()
