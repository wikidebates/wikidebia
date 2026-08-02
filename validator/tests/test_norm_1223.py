from pathlib import Path
import copy

from wikidebia_validator.editorial import validate_introduction_review_data
from wikidebia_validator.report import Report
from wikidebia_validator.package import PackageContext
from wikidebia_validator.wikicode import validate_page


def _review():
    base = {
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
        "documentation_family_notes": {"bibliography":"Une sélection générale suffisamment documentée.","webliography":"Des ressources Web distinctes suffisamment documentées.","videography":"Une sélection vidéo examinée et documentée séparément."},
        "common_acronym": None,
        "common_acronym_used_or_not_applicable": True,
        "topic_is_nominal_label": True,
        "conventional_topic_label_used_or_not_applicable": True,
        "topic_label_rationale": "Le réalisme philosophique est le nom conventionnel de la doctrine.",
        "complete_topic_lowercase_initial_or_justified": True,
        "subsections": [{"title":"Définition","purpose":"Définir le sujet.","necessary_for_understanding":True,"technical_or_specialized":False,"relevance_to_debate_explained":True}],
    }
    en=copy.deepcopy(base); en["language"]="en"; en["subsections"][0]["title"]="Definition"
    return {"review_version":"1.0","normative_revision":"1.2.23","entries":[base,en]}


def test_1223_intro_review_accepts_nominal_topics_and_lowercase_complements():
    issues=validate_introduction_review_data(_review(),{"fr":["Définition"],"en":["Definition"]},norm="1.2.23",complete_topics={"fr":"le réalisme philosophique","en":"philosophical realism"},topics={"fr":"Réalisme philosophique","en":"Philosophical realism"})
    assert not issues


def test_1223_intro_review_rejects_missing_nominal_attestation():
    review=_review(); del review["entries"][0]["topic_is_nominal_label"]
    issues=validate_introduction_review_data(review,{"fr":["Définition"],"en":["Definition"]},norm="1.2.23",complete_topics={"fr":"le réalisme philosophique","en":"philosophical realism"},topics={"fr":"Réalisme philosophique","en":"Philosophical realism"})
    assert any(x["reason"]=="topic_is_nominal_label" for x in issues)


def test_1223_wikicode_rejects_uppercase_complete_topic(tmp_path: Path):
    root=tmp_path
    (root/"manifest.json").write_text('{"normative_versions":{"consolidated_norm":"1.2.23"}}',encoding="utf-8")
    page=root/"debate.wiki"
    page.write_text("{{Débat\n|sujet=Réalisme philosophique\n|sujet-complet=Le réalisme philosophique\n|avancement=Débat construit\n|avertissements-débat=Débat généré par IA\n|introduction={{Sous-partie\n|titre=Définition\n|contenu=Texte\n}}\n|arguments-pour={{Argument pour\n|page=Argument A\n|titre-affiché=Une thèse existe\n}}\n|arguments-contre={{Argument contre\n|page=Argument B\n|titre-affiché=Une objection existe\n}}\n|rubriques=Philosophie\n|mots-clés=réalisme\n|date-création=2026-08-02\n}}\n",encoding="utf-8")
    report=Report("0.4.25",str(root),["wikicode"]); ctx=PackageContext(root,report)
    validate_page(ctx,{"page_id":"demo","page_type":"debate","language":"fr","file_path":"debate.wiki"})
    assert any(i.code=="WDV-EDT-018" and "minuscule" in i.message for i in report.findings)


def test_1223_argument_web_reference_rejects_author_equal_site(tmp_path: Path):
    root=tmp_path
    (root/"manifest.json").write_text('{"normative_versions":{"consolidated_norm":"1.2.23"}}',encoding="utf-8")
    page=root/"argument.wiki"
    page.write_text("{{Argument\n|titre-affiché=Le monde résiste à nos attentes\n|avertissements-argument=Argument généré par IA\n|résumé=Résumé suffisamment développé pour le test.\n|citations=\n|références-sitographiques={{Référence sitographique\n|lien=https://example.org/article\n|page=Un article\n|auteurs=Example\n|site=Example\n|date=2 août 2026\n}}\n|justifications=\n|objections=\n|rubriques=Philosophie\n|mots-clés=réalisme\n|interlangue={{Lien interlangue\n|langue=en\n|page=Argument\n}}\n|date-création=2026-08-02\n}}\n",encoding="utf-8")
    report=Report("0.4.25",str(root),["wikicode"]); ctx=PackageContext(root,report)
    validate_page(ctx,{"page_id":"A0001","page_type":"argument","language":"fr","file_path":"argument.wiki"})
    assert any(i.code=="WDV-DOC-004" and i.details.get("applies_to_argument_pages") is True for i in report.findings)
