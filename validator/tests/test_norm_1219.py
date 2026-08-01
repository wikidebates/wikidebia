from __future__ import annotations

from wikidebia_validator.editorial import displayed_title_argument_issues, validate_individual_review_data


def node(fr_title: str, en_title: str = "Observer agreement indicates public objects"):
    return {
        "id": "A0001",
        "status": "active",
        "fr": {"displayed_title": fr_title, "rubriques": ["Philosophie"]},
        "en": {"displayed_title": en_title, "sections": ["Philosophy"]},
    }


def review(**overrides):
    entry = {
        "id": "A0001",
        "title_decision": "reformulated",
        "title_reason": "Le libellé expose désormais une proposition argumentative complète.",
        "new_displayed_title_fr": "La convergence entre observateurs indique l'existence d'objets publics",
        "new_rubriques": ["Philosophie"],
        "rubric_decision": "retained_after_review",
        "rubric_rationales": {"Philosophie": "Le nœud porte sur la connaissance du réel."},
        "new_displayed_title_en": "Observer agreement indicates public objects",
        "new_sections_en": ["Philosophy"],
        "canonical_referents_explicit_fr": True,
        "canonical_referents_explicit_en": True,
        "displayed_referents_explicit_fr": True,
        "displayed_referents_explicit_en": True,
        "displayed_title_complete_proposition_fr": True,
        "displayed_title_argument_intelligible_fr": True,
        "displayed_title_complete_proposition_en": True,
        "displayed_title_argument_intelligible_en": True,
    }
    entry.update(overrides)
    return {"entries": [entry]}


def test_nominal_french_displayed_titles_are_rejected():
    bad = [
        "La résistance du monde à nos attentes",
        "La convergence entre observateurs",
        "Le succès prédictif et technique des sciences",
        "Les renversements de l'histoire des sciences",
        "La corrélation entre expérience et monde",
    ]
    for title in bad:
        assert "missing_explicit_predicate" in displayed_title_argument_issues(title, "fr")


def test_complete_french_argument_title_is_accepted():
    assert not displayed_title_argument_issues(
        "La convergence entre observateurs indique l'existence d'objets publics", "fr"
    )
    assert not displayed_title_argument_issues(
        "Les renversements scientifiques montrent que le succès d'une théorie ne garantit pas sa vérité", "fr"
    )


def test_nominal_english_displayed_title_is_rejected():
    assert displayed_title_argument_issues("Agreement between observers", "en")
    assert not displayed_title_argument_issues("Agreement between observers indicates public objects", "en")


def test_1219_review_requires_complete_proposition_attestations():
    n = node("La convergence entre observateurs indique l'existence d'objets publics")
    assert not validate_individual_review_data(review(), [n], norm="1.2.19")
    broken = review(displayed_title_argument_intelligible_fr=False)
    issues = validate_individual_review_data(broken, [n], norm="1.2.19")
    assert any(issue["reason"] == "displayed_title_argument_intelligible_fr" for issue in issues)


def test_1218_review_does_not_require_new_attestations():
    n = node("La convergence entre observateurs indique l'existence d'objets publics")
    old = review()
    for field in [
        "displayed_title_complete_proposition_fr",
        "displayed_title_argument_intelligible_fr",
        "displayed_title_complete_proposition_en",
        "displayed_title_argument_intelligible_en",
    ]:
        old["entries"][0].pop(field)
    assert not validate_individual_review_data(old, [n], norm="1.2.18")
