from wikidebia_validator.report import Report
from wikidebia_validator.wikicode import parse_template, validate_template_shape


class Context:
    def __init__(self, norm: str = "1.2.13"):
        self.norm = norm
        self.report = Report("0.4.13", "test-fixture-1213", ["wikicode"])

    def manifest(self):
        return {"normative_versions": {"consolidated_norm": self.norm}}


def page(boundary: str) -> str:
    return (
        "{{Argument\n"
        "|avertissements-argument=Argument généré par IA\n"
        "|résumé=Résumé.\n"
        "|références-bibliographiques={{Référence bibliographique\n"
        "|auteurs=Auteur A\n|ouvrage=Ouvrage A\n|date=25 juin 2012\n}}"
        + boundary
        + "{{Référence bibliographique\n|auteurs=Auteur B\n|ouvrage=Ouvrage B\n|date=26 juin 2012\n}}\n"
        "|rubriques=Société\n|mots-clés=exemple\n|date-création=2026-07-30\n}}\n"
    )


def findings(boundary: str):
    ctx = Context()
    validate_template_shape(ctx, parse_template(page(boundary)), "fr", "argument", "A0001.wiki")
    return [finding for finding in ctx.report.findings if finding.code == "WDV-MWK-018"]


def test_norm_1213_keeps_compact_template_boundary_rule():
    assert findings("") == []
    assert findings("\n")


def test_validator_metadata_reports_0413():
    assert Context().report.validator_version == "0.4.13"
