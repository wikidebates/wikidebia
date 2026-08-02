from __future__ import annotations

from wikidebia_validator.editorial import (
    displayed_title_concision_issues,
    title_copy_ratio,
    validate_individual_review_data,
)


def _node(canonical_fr: str, displayed_fr: str, canonical_en: str, displayed_en: str):
    return {
        "id": "A0001",
        "status": "active",
        "fr": {"canonical_title": canonical_fr, "displayed_title": displayed_fr, "rubriques": ["Philosophie"]},
        "en": {"canonical_title": canonical_en, "displayed_title": displayed_en, "sections": ["Philosophy"]},
    }


def _review(displayed_fr: str, displayed_en: str, **overrides):
    entry = {
        "id": "A0001",
        "title_decision": "reformulated",
        "title_reason": "La formulation a été raccourcie sans perdre la relation argumentative.",
        "new_displayed_title_fr": displayed_fr,
        "new_rubriques": ["Philosophie"],
        "rubric_decision": "retained_after_review",
        "rubric_rationales": {"Philosophie": "Le nœud traite de la connaissance du réel."},
        "new_displayed_title_en": displayed_en,
        "new_sections_en": ["Philosophy"],
        "canonical_referents_explicit_fr": True,
        "canonical_referents_explicit_en": True,
        "displayed_referents_explicit_fr": True,
        "displayed_referents_explicit_en": True,
        "displayed_title_complete_proposition_fr": True,
        "displayed_title_argument_intelligible_fr": True,
        "displayed_title_complete_proposition_en": True,
        "displayed_title_argument_intelligible_en": True,
        "displayed_title_concision_reviewed_fr": True,
        "displayed_title_concision_reviewed_en": True,
    }
    entry.update(overrides)
    return {"entries": [entry]}


def test_1222_detects_exact_copy_and_longer_displayed_title():
    assert displayed_title_concision_issues("Le monde résiste à nos attentes", "Le monde résiste à nos attentes") == ["exact_copy"]
    assert "displayed_longer_than_canonical" in displayed_title_concision_issues(
        "Le monde résiste à nos attentes et révèle son indépendance",
        "Le monde résiste durablement à toutes nos attentes et révèle ainsi clairement son indépendance",
    )


def test_1222_copy_ratio_reports_mechanical_copy():
    nodes = [
        {"fr": {"canonical_title": f"Titre canonique {i}", "displayed_title": f"Titre canonique {i}" if i < 2 else f"Proposition courte {i}"}}
        for i in range(10)
    ]
    assert title_copy_ratio(nodes, "fr") == 0.2


def test_1222_review_requires_concision_attestations():
    n = _node(
        "La convergence intersubjective indique des objets publics indépendants",
        "L'accord perceptif révèle des objets publics indépendants",
        "Intersubjective convergence indicates independent public objects",
        "Perceptual agreement reveals independent public objects",
    )
    ok = _review(n["fr"]["displayed_title"], n["en"]["displayed_title"])
    assert not validate_individual_review_data(ok, [n], norm="1.2.22")
    broken = _review(n["fr"]["displayed_title"], n["en"]["displayed_title"], displayed_title_concision_reviewed_fr=False)
    issues = validate_individual_review_data(broken, [n], norm="1.2.22")
    assert any(issue["reason"] == "displayed_title_concision_reviewed_fr" for issue in issues)


def test_1222_exact_identity_requires_specific_justification_but_1221_does_not():
    canonical_fr = "Le monde résiste à nos attentes et révèle son indépendance"
    canonical_en = "The world resists our expectations and reveals its independence"
    n = _node(canonical_fr, canonical_fr, canonical_en, canonical_en)
    review = _review(canonical_fr, canonical_en)
    issues = validate_individual_review_data(review, [n], norm="1.2.22")
    assert any(issue["reason"] == "displayed_title_identity_justification_fr" for issue in issues)
    assert any(issue["reason"] == "displayed_title_identity_justification_en" for issue in issues)
    assert not validate_individual_review_data(review, [n], norm="1.2.21")


def test_1222_exact_identity_accepts_substantial_justifications():
    canonical_fr = "Le monde résiste à nos attentes et révèle son indépendance"
    canonical_en = "The world resists our expectations and reveals its independence"
    n = _node(canonical_fr, canonical_fr, canonical_en, canonical_en)
    review = _review(
        canonical_fr,
        canonical_en,
        displayed_title_identity_justification_fr="Le titre canonique est déjà bref, propositionnel et ne contient aucun cadrage redondant à retirer.",
        displayed_title_identity_justification_en="The canonical title is already concise, propositional, and contains no redundant framing to remove.",
    )
    assert not validate_individual_review_data(review, [n], norm="1.2.22")
