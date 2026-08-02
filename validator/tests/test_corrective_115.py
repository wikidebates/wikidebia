from pathlib import Path
from wikidebia_validator.editorial import validate_individual_review_data

def node(node_id, title="Titre", rubriques=None):
    return {"id":node_id,"fr":{"displayed_title":title,"rubriques":rubriques or ["Science"]},"en":{"displayed_title":"English title","sections":["Science"]}}

def entry(node_id, title="Titre", rubriques=None):
    return {"id":node_id,"title_decision":"retained_after_review","new_displayed_title_fr":title,"new_rubriques":rubriques or ["Science"],"rubric_decision":"retained_after_review","rubric_rationales":{r:"Justification suffisamment développée pour "+r for r in (rubriques or ["Science"])},"title_reason":"Titre relu et maintenu.","new_displayed_title_en":"English title","new_sections_en":["Science"]}

def test_complete_page_level_review_accepts_ubiquitous_science_and_identical_title():
    nodes=[node("A0001"),node("A0002")]
    review={"entries":[entry("A0001"),entry("A0002")]}
    assert validate_individual_review_data(review,nodes)==[]

def test_missing_review_entry_is_blocking():
    issues=validate_individual_review_data({"entries":[entry("A0001")]},[node("A0001"),node("A0002")])
    assert any(x["reason"]=="coverage" for x in issues)

def test_wrong_rubric_record_is_blocking():
    bad=entry("A0001",rubriques=["Science","Histoire"])
    issues=validate_individual_review_data({"entries":[bad]},[node("A0001")])
    assert any(x["reason"]=="rubriques" for x in issues)

def test_selected_rubric_requires_page_specific_rationale():
    bad=entry("A0001");bad["rubric_rationales"]["Science"]=""
    issues=validate_individual_review_data({"entries":[bad]},[node("A0001")])
    assert any(x["reason"]=="rubric_rationale" for x in issues)

def test_active_norm_is_115():
    root=Path(__file__).parents[1]/"normative_reference"/"01_normes"
    assert sorted(p.name for p in root.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md"))==["WIKIDEBIA_NORME_CONSOLIDEE_1.2.26.md"]
