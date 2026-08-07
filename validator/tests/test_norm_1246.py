from pathlib import Path
from wikidebia_validator.editorial import validate_introduction_review_data


def base_entry(inventory):
    return {"language":"fr","subject_and_scope_defined":True,"debate_question_explained":True,"history_and_evolution_addressed":True,"current_state_addressed_or_not_applicable":True,"stakes_explained":True,"factual_claims_referenced":True,"progression_coherent":True,"no_argument_tree_mirroring":True,"no_topic_specific_checklist":True,"complete_topic_fits_heading":True,"debate_sections_precise":True,"documentation_proportionate_to_literature":True,"documentation_family_notes":{"bibliography":"Une sélection bibliographique suffisamment détaillée.","webliography":"Une sélection sitographique suffisamment détaillée.","videography":"Une sélection vidéographique suffisamment détaillée."},"wikipedia_hover_links_reviewed":True,"specialized_terms_linked_or_explained":True,"common_acronym":None,"common_acronym_used_or_not_applicable":True,"topic_is_nominal_label":True,"conventional_topic_label_used_or_not_applicable":True,"complete_topic_lowercase_initial_or_justified":True,"topic_label_rationale":"Le sujet est formulé sous une forme nominale conventionnelle.","subsections":[{"title":"Définition","purpose":"Définir les notions nécessaires au débat.","necessary_for_understanding":True,"technical_or_specialized":True,"relevance_to_debate_explained":True},{"title":"Méthode","purpose":"Expliquer la méthode des arguments.","necessary_for_understanding":True,"technical_or_specialized":True,"relevance_to_debate_explained":True}],"specialized_term_inventory_reviewed":True,"specialized_term_inventory":inventory}


def issues(inventory, contents):
    review={"schema_version":"1.0","normative_revision":"1.2.46","entries":[base_entry(inventory)]}
    return validate_introduction_review_data(review,{"fr":["Définition","Méthode"]},norm="1.2.46",complete_topics={"fr":"l’existence de Dieu"},topics={"fr":"Dieu"},specialized_term_explanation_policy_revision="1.2.46",actual_contents={"fr":contents})


def good_inventory():
    return [{"subsection_title":"Définition","scan_complete":True,"scan_note":"Toute la sous-partie a été relue pour identifier les notions spécialisées ou opaques.","terms":[{"term":"principe nécessaire","treatment":"wikipedia_link","article":"Nécessité"},{"term":"absolu impersonnel","treatment":"explained_inline","explanation_excerpt":"un absolu impersonnel, c’est-à-dire une réalité qui ne dépend de rien"}]},{"subsection_title":"Méthode","scan_complete":True,"scan_note":"Toute la sous-partie a été relue et les répétitions ont été rattachées à leur premier traitement.","terms":[{"term":"principe nécessaire","treatment":"prior_treatment","prior_subsection_title":"Définition","prior_term":"principe nécessaire"},{"term":"prémisse","treatment":"context_sufficient","justification":"La phrase explique immédiatement qu’il s’agit d’une proposition dont dépend la conclusion."}]}]


def test_1246_accepts_complete_inventory():
    c={"Définition":"Un {{Lien Wikipédia|article=Nécessité|texte-affiché=principe nécessaire}} et un absolu impersonnel, c’est-à-dire une réalité qui ne dépend de rien, sont distingués.","Méthode":"Le principe nécessaire revient dans une prémisse, proposition dont dépend la conclusion."}
    assert not [i for i in issues(good_inventory(),c) if i['reason'].startswith('specialized_') or i['reason']=='undeclared_wikipedia_hover_link']


def test_1246_rejects_undeclared_link():
    c={"Définition":"Un {{Lien Wikipédia|article=Nécessité|texte-affiché=principe nécessaire}} et un {{Lien Wikipédia|article=Absolu (philosophie)|texte-affiché=absolu impersonnel}} sont distingués.","Méthode":"Le principe nécessaire revient dans une prémisse, proposition dont dépend la conclusion."}
    assert any(i['reason']=='undeclared_wikipedia_hover_link' for i in issues(good_inventory(),c))


def test_1246_rejects_missing_subsection_inventory():
    inv=good_inventory()[:1]
    c={"Définition":"Un {{Lien Wikipédia|article=Nécessité|texte-affiché=principe nécessaire}} et un absolu impersonnel, c’est-à-dire une réalité qui ne dépend de rien, sont distingués.","Méthode":"Le principe nécessaire revient dans une prémisse, proposition dont dépend la conclusion."}
    assert any(i['reason']=='specialized_term_inventory_subsections_mismatch' for i in issues(inv,c))


def test_active_norm_is_1246():
    root=Path(__file__).parents[1]/'normative_reference'/'01_normes'
    assert sorted(p.name for p in root.glob('WIKIDEBIA_NORME_CONSOLIDEE_*.md')) == ['WIKIDEBIA_NORME_CONSOLIDEE_1.2.53.md']
