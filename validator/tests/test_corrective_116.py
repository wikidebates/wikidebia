from pathlib import Path
from wikidebia_validator.editorial import validate_individual_review_data


def node(node_id, rubriques=None):
    rs=rubriques or ["Science", "Philosophie"]
    return {"id":node_id,"fr":{"displayed_title":"Titre","rubriques":rs},"en":{"displayed_title":"English title","sections":["Science","Philosophy"][:len(rs)]}}


def entry(node_id, rubriques=None):
    rs=rubriques or ["Science", "Philosophie"]
    reasons={r:f"Justification éditoriale propre à la rubrique {r}" for r in rs}
    sections={"Science":"Science","Philosophie":"Philosophy","Histoire":"History"}
    return {"id":node_id,"title_decision":"retained_after_review","title_reason":"Le titre est déjà clair et concis.","new_displayed_title_fr":"Titre","new_rubriques":rs,"rubric_decision":"retained_after_review","rubric_rationales":reasons,"new_displayed_title_en":"English title","new_sections_en":[sections[r] for r in rs]}


def test_every_selected_rubric_requires_a_rationale():
    bad=entry("A0001",["Science","Philosophie"])
    del bad["rubric_rationales"]["Philosophie"]
    issues=validate_individual_review_data({"entries":[bad]},[node("A0001")])
    assert any(x["reason"]=="rubric_rationale_coverage" for x in issues)


def test_no_rubric_is_treated_specially():
    for rubric,section in [("Science","Science"),("Histoire","History"),("Philosophie","Philosophy")]:
        n={"id":"A0001","fr":{"displayed_title":"Titre","rubriques":[rubric]},"en":{"displayed_title":"English title","sections":[section]}}
        e=entry("A0001",[rubric]); e["new_sections_en"]=[section]
        assert validate_individual_review_data({"entries":[e]},[n])==[]


def test_rationale_for_absent_rubric_is_blocking():
    bad=entry("A0001",["Science"]);bad["rubric_rationales"]["Histoire"]="Justification indue pour une rubrique absente"
    issues=validate_individual_review_data({"entries":[bad]},[node("A0001",["Science"])])
    assert any(x["reason"]=="rubric_rationale_coverage" for x in issues)


def test_runtime_has_no_corpus_specific_constants():
    root=Path(__file__).parents[1]/"src"/"wikidebia_validator"
    text="\n".join(p.read_text(encoding="utf-8") for p in root.glob("*.py"))
    for forbidden in ["science_rationale","parapsychologie_science","2026-07-25","W10.R6","CR-R6"]:
        assert forbidden not in text


def test_active_norm_is_116():
    root=Path(__file__).parents[1]/"normative_reference"/"01_normes"
    assert sorted(p.name for p in root.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md"))==["WIKIDEBIA_NORME_CONSOLIDEE_1.2.17.md"]
