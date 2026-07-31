from wikidebia_validator.editorial import keyword_form_issues


def test_singleton_site_keyword_is_formally_valid():
    # Local frequency is intentionally not part of keyword form validation.
    assert keyword_form_issues(["code ouvert", "reproductibilité"]) == []


def test_site_keyword_still_rejects_sentence_like_phrase():
    issues = keyword_form_issues(["résultat choisi après avoir regardé toutes les analyses", "statistiques"])
    assert "too_many_words" in issues or "too_long" in issues
