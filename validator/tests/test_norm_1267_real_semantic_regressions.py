from __future__ import annotations
import json
from pathlib import Path
from wikidebia_validator.editorial import (
    SEMANTIC_MARKERS,
    bilingual_semantic_marker_losses,
    bilingual_semantic_structure_signals,
    validate_individual_review_data,
)

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "translation_semantic_real_cases_1.0.json"


def test_real_translation_regression_corpus_bad_and_good_pairs():
    data=json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["schema"] == "wikidebia-real-translation-regressions-1.0"
    for case in data["cases"]:
        bad_markers=set(bilingual_semantic_marker_losses(case["fr"],case["bad_en"]))
        good_markers=set(bilingual_semantic_marker_losses(case["fr"],case["good_en"]))
        bad_struct=set(bilingual_semantic_structure_signals(case["fr"],case["bad_en"]))
        good_struct=set(bilingual_semantic_structure_signals(case["fr"],case["good_en"]))
        for expected in case["expected"]:
            if expected.startswith("marker_loss:"):
                label=expected.split(":",1)[1]
                assert label in bad_markers, (case["id"],expected,bad_markers)
                assert label not in good_markers, (case["id"],expected,good_markers)
            else:
                assert expected in bad_struct, (case["id"],expected,bad_struct)
                assert expected not in good_struct, (case["id"],expected,good_struct)


def test_semantic_marker_catalog_has_all_1267_contract_families():
    expected={"attribution","universal_quantifier","existential_quantifier","many_quantifier","several_quantifier","hypothesis_status","interpretation_status","strong_probative_force","frequency_often","frequency_always","necessity","possibility","restriction_only","negation","condition","causal_link","consequence_link","concession","comparison","strong_intensity","immediacy"}
    assert set(SEMANTIC_MARKERS)==expected


from .test_translation_regressions_1260 import _review_entry_1260


def _entry(source_form="question", target_form="proposition", reviewed=True):
    entry=_review_entry_1260()
    entry["displayed_title_source_form_fr"]=source_form
    entry["displayed_title_source_form_en"]=source_form
    entry["displayed_title_target_form_en"]=target_form
    entry["displayed_title_form_change_reviewed_en"]=reviewed
    entry["displayed_title_speech_act_preserved_en"]=reviewed
    entry["displayed_title_form_change_note_en"]="The form change is idiomatic and preserves exactly the same speech act, thesis and logical scope." if reviewed else ""
    return entry


def _node():
    return {"id":"A0001","status":"active","fr":{"canonical_title":"La cause existe","displayed_title":"La cause existe","rubriques":[],"keywords":[]},"en":{"canonical_title":"The cause exists","displayed_title":"The cause exists","sections":[],"keywords":[]}}


def test_idiomatic_form_change_requires_explicit_review_but_is_not_automatically_rejected():
    issues=validate_individual_review_data({"entries":[_entry()]},[_node()],translation_validation_mode="differential",translation_semantic_review_schema_version="1.4")
    assert not [x for x in issues if x["reason"] in {"displayed_title_form_regression","displayed_title_form_change_unreviewed"}]
    issues=validate_individual_review_data({"entries":[_entry(reviewed=False)]},[_node()],translation_validation_mode="differential",translation_semantic_review_schema_version="1.4")
    assert any(x["reason"]=="displayed_title_form_change_unreviewed" for x in issues)


def test_source_proposition_cannot_become_nonproposition_even_with_review():
    entry=_entry("proposition","question",True)
    issues=validate_individual_review_data({"entries":[entry]},[_node()],translation_validation_mode="differential",translation_semantic_review_schema_version="1.4")
    assert any(x["reason"]=="displayed_title_form_regression" for x in issues)


def test_semantic_evidence_lock_checks_target_hashes_and_risk_coverage():
    import hashlib
    from wikidebia_validator.coherence import semantic_evidence_lock_issues
    h=lambda x: hashlib.sha256(str(x).encode()).hexdigest()
    lock={"debate":{"canonical_title":"Debate title","topic":"Topic","complete_topic":"the topic","introduction":"Introduction text",
                    "field_sha256":{"en_canonical_title":h("Debate title"),"en_topic":h("Topic"),"en_complete_topic":h("the topic"),"en_introduction":h("Introduction text")},
                    "debate_field_semantic_risks":["topic:marker_loss:frequency_always"],"debate_field_semantic_risk_reviewed":True,
                    "debate_field_semantic_risk_evidence":[{"risk":"topic:marker_loss:frequency_always","source_excerpt":"Toujours le sujet","target_excerpt":"Topic","note":"The frequency shift was explicitly reviewed."}]},
          "arguments":[{"id":"A1","canonical_title":"Claim exists","displayed_title":"Claim exists","summary":"Summary exists",
                        "field_sha256":{"en_canonical_title":h("Claim exists"),"en_displayed_title":h("Claim exists"),"en_summary":h("Summary exists")},
                        "semantic_risks":["marker_loss:necessity"],"semantic_risk_reviewed":True,
                        "semantic_risk_evidence":[{"risk":"marker_loss:necessity","source_excerpt":"doit exister","target_excerpt":"exists","note":"Necessity was reviewed against the source."}]}]}
    assert semantic_evidence_lock_issues(lock)==[]
    lock["arguments"][0]["summary"]="Mutated summary"
    issues=semantic_evidence_lock_issues(lock)
    assert any(x["reason"]=="argument_field_sha256" for x in issues)
