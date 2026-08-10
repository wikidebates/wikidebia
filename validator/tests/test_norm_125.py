from wikidebia_validator.editorial import _validate_intro_references
from wikidebia_validator.report import Report


class FakeContext:
    def __init__(self, text: str):
        self.text = text
        self.report = Report("0.4.5", "test-fixture", ["editorial"])

    def manifest(self):
        return {
            "normative_versions": {"consolidated_norm": "1.2.5"},
            "pages": [{"page_type": "debate", "language": "fr", "file_path": "output/fr/debate/debate.wiki"}],
        }

    def exists(self, rel):
        return rel == "output/fr/debate/debate.wiki"

    def read_text(self, rel):
        return self.text


def _page(content: str) -> str:
    return "{{Débat\n|sujet=Exemple\n|sujet-développé=la question d’exemple\n|avancement=Débat construit\n|avertissements-débat=Débat généré par IA\n|introduction={{Sous-partie\n|titre=Définition\n|contenu=" + content + "\n}}\n|arguments-pour={{Argument pour\n|page=Une raison favorable complète\n|titre-affiché=Une raison favorable\n}}\n|arguments-contre={{Argument contre\n|page=Une raison défavorable complète\n|titre-affiché=Une raison défavorable\n}}\n|rubriques=Philosophie\n|mots-clés=concept\n|interlangue={{Lien interlangue\n|langue=en\n|page=Should the example proposition be accepted?\n}}\n|date-création=2026-07-28\n}}\n"


def test_norm_125_accepts_conceptual_introduction_without_inline_reference():
    ctx = FakeContext(_page("Cette sous-partie définit les termes employés sans formuler de fait externe."))
    metrics = _validate_intro_references(ctx, ctx.manifest(), {"introduction_references": {"required": True}})
    assert metrics["fr"]["ref_calls"] == 0
    assert not any(f.code == "WDV-EDT-010" for f in ctx.report.findings)


def test_norm_125_rejects_references_tag_even_without_inline_quota():
    ctx = FakeContext(_page("Définition conceptuelle.<references />"))
    _validate_intro_references(ctx, ctx.manifest(), {"introduction_references": {"required": True}})
    assert any(f.code == "WDV-EDT-010" for f in ctx.report.findings)


def test_norm_125_control_must_still_be_activated():
    ctx = FakeContext(_page("Définition conceptuelle."))
    _validate_intro_references(ctx, ctx.manifest(), {"introduction_references": {"required": False}})
    assert any(f.code == "WDV-EDT-010" for f in ctx.report.findings)


def test_norm_125_schema_accepts_control_without_legacy_minimum(tmp_path):
    import json
    from tests.helpers import create_graph_package, dump
    from wikidebia_validator.validator import validate_package

    create_graph_package(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    manifest["normative_versions"]["consolidated_norm"] = "1.2.5"
    manifest["editorial_controls"] = {
        "creation_date": "2026-07-23",
        "individual_review_path": "reports/individual_review.json",
        "individual_review_report_path": "reports/individual_review_report.json",
        "keyword_vocabulary_path": "data/keyword_vocabulary.json",
        "required_reports": [],
        "debate_documentation": {
            "min_subsections": 1,
            "min_references": 0,
            "reject_singleton_bucket_pattern": True,
            "profile_rationale": "Profil local minimal pour le paquet d’exemple.",
        },
        "introduction_references": {"required": True},
        "introduction_review_path": "reports/introduction_review.json",
    }
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["schema"])
    assert not any(f.code == "WDV-SCH-003" for f in report.findings)


def test_old_norm_metadata_does_not_activate_schema_requirement(tmp_path):
    import json
    from tests.helpers import create_graph_package, dump
    from wikidebia_validator.validator import validate_package

    create_graph_package(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    manifest["normative_versions"]["consolidated_norm"] = "1.2.5"
    manifest["editorial_controls"] = {
        "creation_date": "2026-07-23",
        "individual_review_path": "reports/individual_review.json",
        "individual_review_report_path": "reports/individual_review_report.json",
        "keyword_vocabulary_path": "data/keyword_vocabulary.json",
        "required_reports": [],
        "debate_documentation": {
            "min_subsections": 1,
            "min_references": 0,
            "reject_singleton_bucket_pattern": True,
            "profile_rationale": "Profil local minimal pour le paquet d’exemple.",
        },
        "introduction_references": {"required": True},
    }
    dump(tmp_path / "manifest.json", manifest)
    report = validate_package(tmp_path, scopes=["schema"])
    assert not any(f.code == "WDV-SCH-003" for f in report.findings)
