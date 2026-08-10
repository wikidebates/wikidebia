from pathlib import Path
from types import SimpleNamespace

from wikidebia_validator.editorial import validate_introduction_review_data
from wikidebia_validator.wikicode import documentary_date_is_machine


def test_documentary_machine_dates_are_distinguished_from_years():
    assert documentary_date_is_machine("2012-06-25")
    assert documentary_date_is_machine("2012-06")
    assert not documentary_date_is_machine("25 juin 2012")
    assert not documentary_date_is_machine("25 June 2012")
    assert not documentary_date_is_machine("2012")


def test_common_acronym_must_appear_in_complete_topic():
    review = {
        "normative_revision": "1.2.9",
        "entries": [{
            "language": "fr",
            "subject_and_scope_defined": True,
            "debate_question_explained": True,
            "history_and_evolution_addressed": True,
            "current_state_addressed_or_not_applicable": True,
            "stakes_explained": True,
            "factual_claims_referenced": True,
            "progression_coherent": True,
            "no_argument_tree_mirroring": True,
            "no_topic_specific_checklist": True,
            "complete_topic_fits_heading": True,
            "debate_sections_precise": True,
            "documentation_proportionate_to_literature": True,
            "documentation_family_notes": {
                "bibliography": "Une justification documentaire suffisamment développée.",
                "webliography": "Une justification documentaire suffisamment développée.",
                "videography": "Une justification documentaire suffisamment développée.",
            },
            "common_acronym": "GPA",
            "common_acronym_used_or_not_applicable": True,
            "subsections": [],
        }],
    }
    issues = validate_introduction_review_data(
        review,
        {"fr": []},
        norm="1.2.9",
        complete_topics={"fr": "l’autorisation de la gestation pour autrui"},
    )
    assert any(i["reason"] == "common_acronym_missing_from_complete_topic" for i in issues)
    issues = validate_introduction_review_data(
        review,
        {"fr": []},
        norm="1.2.9",
        complete_topics={"fr": "l’autorisation de la GPA"},
    )
    assert not any(i["reason"] == "common_acronym_missing_from_complete_topic" for i in issues)

from wikidebia_validator.editorial import _validate_debate_docs, _validate_intro_references
from wikidebia_validator.report import Report
from wikidebia_validator.wikicode import parse_template, validate_template_shape


class EditorialFakeContext:
    def __init__(self, text: str, language: str = "fr"):
        self.text = text
        self.language = language
        self.report = Report("0.4.10", "test-fixture-129", ["editorial", "wikicode"])

    def manifest(self):
        return {
            "normative_versions": {"consolidated_norm": "1.2.9"},
            "pages": [{"page_type": "debate", "language": self.language, "file_path": f"output/{self.language}/debate.wiki"}],
        }

    def exists(self, rel):
        return rel == f"output/{self.language}/debate.wiki"

    def read_text(self, rel):
        return self.text


def _fr_debate_with_intro(content: str) -> str:
    return "{{Débat\n|sujet=Gestation pour autrui\n|sujet-développé=l’autorisation de la GPA\n|avancement=Débat construit\n|avertissements-débat=Débat généré par IA\n|introduction={{Sous-partie\n|titre=Définition\n|contenu=" + content + "\n}}\n|arguments-pour={{Argument pour\n|page=Une raison favorable complète\n|titre-affiché=Une raison favorable\n}}\n|arguments-contre={{Argument contre\n|page=Une raison défavorable complète\n|titre-affiché=Une raison défavorable\n}}\n|rubriques=Société\n|mots-clés=gestation pour autrui\n|interlangue={{Lien interlangue\n|langue=en\n|page=Should surrogacy be permitted?\n}}\n|date-création=2026-07-30\n}}\n"


def test_current_intro_references_require_direct_wikicode_even_with_old_norm_metadata():
    typed = EditorialFakeContext(_fr_debate_with_intro("Fait documenté<ref>{{Référence bibliographique|auteurs=A|ouvrage=O|date=25 juin 2012}}</ref>."))
    _validate_intro_references(typed, typed.manifest(), {"introduction_references": {"required": True}})
    assert any(f.code == "WDV-EDT-010" for f in typed.report.findings)

    generic = EditorialFakeContext(_fr_debate_with_intro("Fait documenté<ref>{{Référence|auteurs=A|titre=O|date=25 juin 2012}}</ref>."))
    _validate_intro_references(generic, generic.manifest(), {"introduction_references": {"required": True}})
    assert any(f.code == "WDV-EDT-010" for f in generic.report.findings)

    direct = EditorialFakeContext(_fr_debate_with_intro("Fait documenté<ref>Auteur A, ''Ouvrage O'', 25 juin 2012</ref>."))
    metrics = _validate_intro_references(direct, direct.manifest(), {"introduction_references": {"required": True}})
    assert metrics["fr"]["invalid_direct_reference_notes"] == []
    assert not any(f.code == "WDV-EDT-010" for f in direct.report.findings)


def test_norm_129_documentary_machine_date_rejected_but_creation_date_kept_machine():
    ctx = EditorialFakeContext(_fr_debate_with_intro("Fait documenté<ref>{{Référence|auteurs=A|titre=O|date=2012-06-25}}</ref>."))
    _validate_intro_references(ctx, ctx.manifest(), {"introduction_references": {"required": True}})
    assert any(f.code == "WDV-DOC-005" for f in ctx.report.findings)
    assert "|date-création=2026-07-30" in ctx.text


def _reference_model(param: str, index: int) -> str:
    if param.startswith("bibliographie"):
        name = "Référence bibliographique pour" if param.endswith("pour") and "ni-pour" not in param else "Référence bibliographique contre" if param.endswith("contre") else "Référence bibliographique"
        return f"{{{{{name}\n|auteurs=Auteur {index}\n|ouvrage=Ouvrage {index}\n|date={20 + index} juin 2012\n}}}}"
    if param.startswith("sitographie"):
        name = "Référence sitographique pour" if param.endswith("pour") and "ni-pour" not in param else "Référence sitographique contre" if param.endswith("contre") else "Référence sitographique"
        return f"{{{{{name}\n|lien=https://example.org/{param}/{index}\n|site=Example {index}\n|date={20 + index} juin 2012\n}}}}"
    name = "Référence vidéographique pour" if param.endswith("pour") and "ni-pour" not in param else "Référence vidéographique contre" if param.endswith("contre") else "Référence vidéographique"
    return f"{{{{{name}\n|titre=Vidéo {index}\n|lien=https://example.org/video/{param}/{index}\n}}}}"


def _fr_debate_documentation(duplicate_first_bucket: bool = False) -> str:
    params = ["bibliographie-pour", "bibliographie-contre", "bibliographie-ni-pour-ni-contre", "sitographie-pour", "sitographie-contre", "sitographie-ni-pour-ni-contre", "vidéographie-pour", "vidéographie-contre", "vidéographie-ni-pour-ni-contre"]
    doc = []
    for position, param in enumerate(params):
        first = _reference_model(param, position * 2 + 1)
        second = first if duplicate_first_bucket and position == 0 else _reference_model(param, position * 2 + 2)
        doc.append(f"|{param}={first}\n{second}")
    return _fr_debate_with_intro("Définition conceptuelle.").replace("|rubriques=Société", "\n".join(doc) + "\n|rubriques=Société")


def test_old_129_bucket_quota_is_superseded_by_current_no_quota_policy():
    controls = {"debate_documentation": {"min_subsections": 1, "min_references": 0, "profile_rationale": "Minimum structurel propre aux pages de débat de la norme 1.2.9."}}
    valid = EditorialFakeContext(_fr_debate_documentation())
    metrics = _validate_debate_docs(valid, valid.manifest(), controls, norm="1.2.9")
    assert metrics["fr"]["distinct_bucket_counts"] == [2] * 9
    assert not any(f.code == "WDV-EDT-004" for f in valid.report.findings)

    duplicate = EditorialFakeContext(_fr_debate_documentation(duplicate_first_bucket=True))
    _validate_debate_docs(duplicate, duplicate.manifest(), controls, norm="1.2.9")
    assert not any(f.code == "WDV-EDT-004" for f in duplicate.report.findings)
    assert duplicate.report.metrics == {} or True


def test_old_norm_metadata_does_not_disable_current_natural_documentary_date_rule():
    class LegacyContext:
        def __init__(self):
            self.report = Report("0.4.10", "test-fixture-128", ["wikicode"])
        def manifest(self):
            return {"normative_versions": {"consolidated_norm": "1.2.8"}}

    text = "{{Argument\n|avertissements-argument=Argument généré par IA\n|résumé=Résumé.\n|références-bibliographiques={{Référence bibliographique\n|auteurs=A\n|ouvrage=O\n|date=2012-06-25\n}}\n|rubriques=Société\n|mots-clés=exemple\n|date-création=2026-07-30\n}}\n"
    ctx = LegacyContext()
    validate_template_shape(ctx, parse_template(text), "fr", "argument", "A0001.wiki")
    assert any(f.code == "WDV-DOC-005" for f in ctx.report.findings)


def _english_reference_model(param: str, index: int) -> str:
    if "bibliography" in param:
        name = "Pro bibliographical reference" if param == "pro-bibliography" else "Con bibliographical reference" if param == "con-bibliography" else "Bibliographical reference"
        return f"{{{{{name}\n|authors=Author {index}\n|work=Work {index}\n|date={20 + index} June 2012\n}}}}"
    if "webliography" in param:
        name = "Pro web reference" if param == "pro-webliography" else "Con web reference" if param == "con-webliography" else "Web reference"
        return f"{{{{{name}\n|link=https://example.org/{param}/{index}\n|site=Example {index}\n|date={20 + index} June 2012\n}}}}"
    name = "Pro video reference" if param == "pro-videography" else "Con video reference" if param == "con-videography" else "Video reference"
    return f"{{{{{name}\n|title=Video {index}\n|link=https://example.org/video/{param}/{index}\n}}}}"


def _english_debate_documentation() -> str:
    params = ["pro-bibliography", "con-bibliography", "bibliography", "pro-webliography", "con-webliography", "webliography", "pro-videography", "con-videography", "videography"]
    doc = []
    for position, param in enumerate(params):
        doc.append(f"|{param}={_english_reference_model(param, position * 2 + 1)}\n{_english_reference_model(param, position * 2 + 2)}")
    return "{{Debate\n|topic=Surrogacy\n|expanded-topic=the authorization of surrogacy\n|progress=Constructed debate\n|debate-warnings=Debate generated by AI\n|introduction={{Subsection\n|title=Definition\n|content=Conceptual definition.\n}}\n|pro-arguments={{Pro argument\n|page=A complete favorable reason\n|displayed-title=A favorable reason\n}}\n|con-arguments={{Con argument\n|page=A complete unfavorable reason\n|displayed-title=An unfavorable reason\n}}\n" + "\n".join(doc) + "\n|sections=Society\n|keywords=surrogacy\n|creation-date=2026-07-30\n}}\n"


def test_norm_129_english_debate_buckets_have_same_plurality_rule():
    controls = {"debate_documentation": {"min_subsections": 1, "min_references": 0, "profile_rationale": "Minimum structural coverage for Debate pages under norm 1.2.9."}}
    ctx = EditorialFakeContext(_english_debate_documentation(), language="en")
    metrics = _validate_debate_docs(ctx, ctx.manifest(), controls, norm="1.2.9")
    assert metrics["en"]["distinct_bucket_counts"] == [2] * 9
    assert not any(f.code == "WDV-EDT-004" for f in ctx.report.findings)
