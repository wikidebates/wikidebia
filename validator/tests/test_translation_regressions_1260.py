from wikidebia_validator.editorial import (
    bilingual_semantic_marker_losses,
    bilingual_semantic_structure_signals,
    displayed_title_translation_form_regression,
)


def test_regression_generic_deity_must_not_become_proper_God():
    assert 'generic_deity_to_proper_God' in bilingual_semantic_structure_signals(
        "Il faut se méfier des analogies utilisées pour montrer l'existence d'un dieu",
        "One should be wary of analogies used to show God's existence",
    )


def test_regression_attributed_property_must_not_become_direct_property():
    assert 'attributed_property_to_direct_property' in bilingual_semantic_structure_signals(
        "L'autodétermination contredit l'omniscience attribuée à Dieu",
        "Human self-determination contradicts divine omniscience",
    )


def test_regression_inference_must_not_become_categorical_assertion():
    assert 'epistemic_inference_to_categorical_assertion' in bilingual_semantic_structure_signals(
        "L'absence de traces conduit à considérer le récit comme mythologique",
        "The lack of evidence makes the narrative mythological",
    )


def test_regression_quantity_must_not_become_sufficiency():
    assert 'quantity_to_sufficiency' in bilingual_semantic_structure_signals(
        "La sélection naturelle n'a besoin que du hasard et de beaucoup de temps",
        "Natural selection needs only chance and sufficient time",
    )


def test_regression_equivalence_must_not_be_weakened_to_same_problem():
    assert 'equivalence_weakened_to_same_problem' in bilingual_semantic_structure_signals(
        "Prétendre qu'une chose n'a pas de cause ou qu'un dieu n'a pas de cause, cela revient au même",
        "An uncaused reality and an uncaused God raise the same problem",
    )


def test_regression_predicate_subject_shift_God_to_belief():
    assert 'predicate_subject_shift_God_to_belief' in bilingual_semantic_structure_signals(
        "Si Dieu ne peut pas être prouvé, il est un objet irrationnel",
        "If God cannot be proved, belief in him is irrational",
    )


def test_regression_preserve_supposed_and_all_markers():
    assert 'attribution' in bilingual_semantic_marker_losses(
        "Dieu est censé être omnipotent",
        "God is omnipotent",
    )
    assert 'universal_quantifier' in bilingual_semantic_marker_losses(
        "La simplicité divine rend nécessaires tous les actes de Dieu",
        "Divine simplicity makes God's acts necessary",
    )


def test_translation_mode_blocks_only_form_degradation_not_inherited_form():
    # Source and target are both thematic labels: no retroactive creation-rule repair.
    assert displayed_title_translation_form_regression("Hans Jonas sur la bonté de Dieu", "Hans Jonas on God's goodness") == []
    # A source proposition degraded into a fragment is still a regression.
    assert displayed_title_translation_form_regression(
        "L'omniscience attribuée à Dieu contredit la liberté humaine",
        "Divine omniscience and human freedom",
    )


def _review_entry_1260():
    return {
        'id':'A0001','title_decision':'retained_after_review','title_reason':'The source and target titles were compared directly and retained after bilingual review.',
        'canonical_referents_explicit_fr':True,'canonical_referents_explicit_en':True,
        'displayed_referents_explicit_fr':True,'displayed_referents_explicit_en':True,
        'displayed_title_argument_intelligible_fr':True,'displayed_title_argument_intelligible_en':True,
        'displayed_title_source_form_reviewed_fr':True,'displayed_title_source_form_reviewed_en':True,
        'displayed_title_no_formal_regression_en':True,'displayed_title_semantic_inventory_reviewed_en':True,
        'displayed_title_source_form_fr':'proposition','displayed_title_source_form_en':'proposition','displayed_title_target_form_en':'proposition',
        'displayed_title_complete_proposition_en':True,'displayed_title_semantic_inventory_note_en':'Subject, predicate, scope, modality and logical force were compared against the French source.',
        'canonical_title_semantic_inventory_reviewed_en':True,'canonical_title_semantically_equivalent_en':True,
        'canonical_title_semantic_inventory_note_en':'Subject, predicate, scope and modality were compared against the French source.',
        'canonical_title_subject_preserved_en':True,'canonical_title_predicate_preserved_en':True,
        'canonical_title_scope_preserved_en':True,'canonical_title_modality_preserved_en':True,
        'displayed_title_subject_preserved_en':True,'displayed_title_predicate_preserved_en':True,
        'displayed_title_scope_preserved_en':True,'displayed_title_modality_preserved_en':True,
        'displayed_title_concision_reviewed_fr':True,'displayed_title_concision_reviewed_en':True,
        'displayed_title_semantically_equivalent_fr':True,'displayed_title_semantically_equivalent_en':True,
        'displayed_title_improves_readability_when_distinct_fr':False,'displayed_title_improves_readability_when_distinct_en':False,
        'displayed_title_identity_justification_fr':'','displayed_title_identity_justification_en':'',
        'new_displayed_title_fr':'La cause existe','new_displayed_title_en':'The cause exists',
        'new_rubriques':[],'new_sections_en':[],'new_keywords_fr':[],'new_keywords_en':[],
        'keywords_ordered_by_relevance_fr':True,'keywords_ordered_by_relevance_en':True,
        'keyword_order_rationale_fr':'Ordre validé.','keyword_order_rationale_en':'Reviewed order.',
    }


def test_structured_semantic_review_12_requires_subject_predicate_scope_modality():
    from wikidebia_validator.editorial import validate_individual_review_data
    node={'id':'A0001','status':'active','fr':{'canonical_title':'La cause existe','displayed_title':'La cause existe','rubriques':[],'keywords':[]},'en':{'canonical_title':'The cause exists','displayed_title':'The cause exists','sections':[],'keywords':[]}}
    entry=_review_entry_1260()
    entry['canonical_title_scope_preserved_en']=False
    issues=validate_individual_review_data({'entries':[entry]},[node],translation_validation_mode='differential',translation_semantic_review_schema_version='1.2')
    assert any(i.get('reason')=='canonical_title_scope_preserved_en' for i in issues)
