from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report
from wikidebia_validator.wikicode import parse_template, validate_template_shape, _validate_debate_content


def context(norm: str = "1.2.17") -> PackageContext:
    return PackageContext(
        root=Path("."),
        report=Report("0.4.18", ".", ["wikicode"]),
        cache={"manifest.json": {"normative_versions": {"consolidated_norm": norm}}},
    )


def debate(article: str, related: str = "") -> str:
    return """{{Débat
|sujet=Sujet
|sujet-complet=la question du sujet
|avancement=Débat construit
|avertissements-débat=Débat généré par IA
|introduction={{Sous-partie
|titre=Définition
|contenu=Texte.
}}
%s
|arguments-pour={{Argument pour
|page=Pour
|titre-affiché=Pour
}}
|arguments-contre={{Argument contre
|page=Contre
|titre-affiché=Contre
}}
%s
|rubriques=Société
|mots-clés=sujet
|interlangue={{Lien interlangue
|langue=en
|page=Topic
}}
|date-création=2026-08-01
}}""" % (article, related)


def test_wikipedia_parameter_is_required_and_nonempty():
    ctx = context()
    tmpl = parse_template(debate(""))
    validate_template_shape(ctx, tmpl, "fr", "debate", "debate.wiki")
    assert any(issue.code == "WDV-MWK-004" and "articles-Wikipédia" in issue.message for issue in ctx.report.findings)


def test_valid_wikipedia_article_passes_specific_gate():
    ctx = context()
    tmpl = parse_template(debate("|articles-Wikipédia={{Article Wikipédia\n|page=Philosophie\n}}"))
    validate_template_shape(ctx, tmpl, "fr", "debate", "debate.wiki")
    _validate_debate_content(ctx, tmpl, "debate.wiki", "fr", {"graph": {"occurrences": [], "nodes": []}}, {"creation_date": "2026-08-01"})
    assert not any(issue.code == "WDV-MWK-019" for issue in ctx.report.findings)


def test_related_debates_parameter_is_forbidden():
    ctx = context()
    tmpl = parse_template(debate("|articles-Wikipédia={{Article Wikipédia\n|page=Philosophie\n}}", "|débats-connexes={{Débat connexe\n|page=Autre débat\n}}"))
    validate_template_shape(ctx, tmpl, "fr", "debate", "debate.wiki")
    assert any(issue.code == "WDV-MWK-003" and "débats-connexes" in issue.message for issue in ctx.report.findings)


def test_json_author_array_is_rejected():
    ctx = context()
    text = debate("|articles-Wikipédia={{Article Wikipédia\n|page=Philosophie\n}}")
    text = text.replace("|rubriques=Société", "|sitographie-ni-pour-ni-contre={{Référence sitographique\n|lien=https://example.test\n|auteurs=[\"L'Encyclopédie philosophique\"]\n|site=L'Encyclopédie philosophique\n}}\n|rubriques=Société")
    tmpl = parse_template(text)
    validate_template_shape(ctx, tmpl, "fr", "debate", "debate.wiki")
    assert any(issue.code == "WDV-DOC-006" for issue in ctx.report.findings)


def test_rules_are_not_retroactive_to_1216():
    ctx = context("1.2.16")
    tmpl = parse_template(debate(""))
    validate_template_shape(ctx, tmpl, "fr", "debate", "debate.wiki")
    assert not any(issue.code in {"WDV-MWK-019", "WDV-DOC-006"} for issue in ctx.report.findings)
    assert not any("articles-Wikipédia" in issue.message and issue.code == "WDV-MWK-004" for issue in ctx.report.findings)
