from wikidebia_validator.editorial import displayed_title_issues, keyword_form_issues


def test_complex_french_quotes_are_rejected():
    assert "complex_quotes" in displayed_title_issues("Le terme « effet de seuil » est défini négativement", "fr")


def test_straight_ascii_quotes_are_accepted():
    assert "complex_quotes" not in displayed_title_issues('Le terme "effet de seuil" est défini négativement', "fr")


def test_unbalanced_ascii_quotes_are_rejected():
    assert "unbalanced_quotes" in displayed_title_issues('Le terme "effet de seuil est défini négativement', "fr")


def test_keyword_complexity_is_bounded():
    assert "too_many_words" in keyword_form_issues(["mot clé beaucoup trop long et spécifique", "statistiques"])


def test_two_to_four_thematic_keywords_are_accepted():
    assert keyword_form_issues(["statistiques", "biais de recherche"]) == []
    assert keyword_form_issues(["réplication", "science ouverte", "statistiques", "méthode expérimentale"]) == []
