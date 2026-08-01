from __future__ import annotations

from wikidebia_validator.wikicode import parse_template, validate_template_shape
from tests.test_norm_1217 import context, debate


def with_authors(value: str) -> str:
    text = debate("|articles-Wikipédia={{Article Wikipédia\n|page=Philosophie\n}}")
    return text.replace("|rubriques=Société", f"|sitographie-ni-pour-ni-contre={{{{Référence sitographique\n|lien=https://example.test\n|auteurs={value}\n|site=Exemple\n}}}}\n|rubriques=Société")


def issues(value: str, norm: str = "1.2.18"):
    ctx = context(norm)
    validate_template_shape(ctx, parse_template(with_authors(value)), "fr", "debate", "debate.wiki")
    return ctx.report.findings


def test_comma_space_author_separator_is_accepted():
    assert not any(i.code == "WDV-DOC-007" for i in issues("Auteur A, Auteur B"))

def test_semicolon_author_separator_is_rejected():
    assert any(i.code == "WDV-DOC-007" for i in issues("Auteur A ; Auteur B"))

def test_comma_without_space_is_rejected():
    assert any(i.code == "WDV-DOC-007" for i in issues("Auteur A,Auteur B"))

def test_space_before_comma_is_rejected():
    assert any(i.code == "WDV-DOC-007" for i in issues("Auteur A , Auteur B"))

def test_fullwidth_comma_is_rejected():
    assert any(i.code == "WDV-DOC-007" for i in issues("Auteur A， Auteur B"))

def test_separator_rule_is_not_retroactive_to_1217():
    assert not any(i.code == "WDV-DOC-007" for i in issues("Auteur A ; Auteur B", "1.2.17"))
