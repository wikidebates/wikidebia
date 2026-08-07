from wikidebia_validator.report import Report
from wikidebia_validator.wikicode import parse_template, validate_template_shape


class Context:
    def __init__(self, norm: str = "1.2.11"):
        self.norm = norm
        self.report = Report("0.4.11", "test-fixture-1211", ["wikicode"])

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


def findings(boundary: str, norm: str = "1.2.11"):
    ctx = Context(norm)
    validate_template_shape(ctx, parse_template(page(boundary)), "fr", "argument", "A0001.wiki")
    return [f for f in ctx.report.findings if f.code == "WDV-MWK-018"]


def test_norm_1211_accepts_exact_compact_boundary():
    assert findings("") == []


def test_norm_1211_rejects_lf_and_horizontal_whitespace_between_templates():
    result = findings("  \n\t")
    assert result
    assert findings(" ")
    assert result[0].details["replacement"] == "}}{{"


def test_norm_1211_rejects_crlf_and_multiple_blank_lines_between_templates():
    assert findings("\r\n  \r\n")


def test_old_norm_metadata_does_not_disable_adjacent_template_rule():
    assert any(f.code == "WDV-MWK-018" for f in findings("\n", norm="1.2.10"))
