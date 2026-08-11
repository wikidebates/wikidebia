from __future__ import annotations

from wikidebia_validator.editorial import keyword_form_issues, validate_individual_review_data
from .current_policy_helpers import complete_individual_entry


def _node():
    return {
        "id": "A0001",
        "status": "active",
        "fr": {"displayed_title": "Une réduction des inégalités", "rubriques": ["Société"]},
        "en": {"displayed_title": "Reducing inequality", "sections": ["Society"]},
    }


def _entry():
    node = _node()
    entry = {
        "id": "A0001",
        "title_decision": "retained_after_review",
        "title_reason": "Le titre affiché historique est conservé ; aucune faute ni anomalie manifeste ne justifie une réécriture.",
        "new_displayed_title_fr": "Une réduction des inégalités",
        "new_rubriques": ["Société"],
        "rubric_decision": "retained_after_review",
        "rubric_rationales": {"Société": "La rubrique décrit directement l'enjeu social."},
        "canonical_referents_explicit_fr": True,
        "canonical_referents_explicit_en": True,
        "displayed_referents_explicit_fr": True,
        "displayed_referents_explicit_en": True,
        "displayed_title_complete_proposition_fr": False,
        "displayed_title_argument_intelligible_fr": True,
        "displayed_title_complete_proposition_en": True,
        "displayed_title_argument_intelligible_en": True,
    }
    return complete_individual_entry(entry, node)


def test_preexisting_french_page_does_not_require_complete_proposition_attestation():
    issues = validate_individual_review_data(
        {"entries": [_entry()]}, [_node()], english_deferred=True, preexisting_node_ids={"A0001"}
    )
    assert not any(issue.get("reason") == "displayed_title_complete_proposition_fr" for issue in issues)


def test_new_french_page_still_requires_complete_proposition_attestation():
    issues = validate_individual_review_data(
        {"entries": [_entry()]}, [_node()], english_deferred=True, preexisting_node_ids=set()
    )
    assert any(issue.get("reason") == "displayed_title_complete_proposition_fr" for issue in issues)


def test_preexisting_keyword_count_is_not_a_creation_quota():
    five = ["revenu de base", "redistribution", "travail", "pauvreté", "protection sociale"]
    assert "count" in keyword_form_issues(five, enforce_count=True)
    assert "count" not in keyword_form_issues(five, enforce_count=False)
