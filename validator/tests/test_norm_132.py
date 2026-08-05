from wikidebia_validator.editorial import keyword_capitalization_issues


def test_common_keywords_require_lowercase_initial():
    assert keyword_capitalization_issues("revenu", "noun") == []
    assert "common_keyword_initial_uppercase" in keyword_capitalization_issues("Revenu", "noun")
    assert keyword_capitalization_issues("philosophie politique", "noun_phrase") == []
    assert "common_keyword_initial_uppercase" in keyword_capitalization_issues("Philosophie politique", "noun_phrase")


def test_proper_names_and_acronyms_keep_canonical_capitals():
    assert keyword_capitalization_issues("Dieu", "proper_name") == []
    assert keyword_capitalization_issues("Union européenne", "proper_name") == []
    assert keyword_capitalization_issues("eBay", "proper_name") == []
    assert keyword_capitalization_issues("ONU", "acronym") == []
    assert "acronym_not_uppercase" in keyword_capitalization_issues("Onu", "acronym")
