from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


content = load_module("wikidebia_content_review")
metadata = sys.modules.get("wikidebia_editorial_review") or load_module("wikidebia_editorial_review")
workspace_tool = sys.modules.get("wikidebia_editorial_workspace") or load_module("wikidebia_editorial_workspace")
common = sys.modules["wikidebia_corpus_build"]

def fake_validator(*args, **kwargs):
    return {"validator_version": "0.4.29", "result": "passed", "summary": {"errors": 0, "warnings": 0}}

metadata._run_validator = fake_validator
content._run_validator = fake_validator

from test_wikidebia_editorial_review import make_workspace, complete_review  # noqa: E402


def make_metadata_applied(tmp_path: Path) -> tuple[Path, Path, str]:
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    finalized = metadata.finalize_review(project, "debat_test", work_id)
    metadata.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    return project, workspace, work_id


def source_row(source_id: str, source_type: str, usages: list[dict[str, object]]) -> dict[str, object]:
    index = int(source_id[1:])
    metadata_row = {
        "authors": [f"Auteur {index}"],
        "article": None,
        "work": None,
        "volume": None,
        "issue": None,
        "location": None,
        "publisher": None,
        "place": None,
        "date": "3 août 2026",
        "link": None,
        "page": None,
        "site": None,
        "title": None,
    }
    if source_type == "bibliography":
        metadata_row["work"] = f"Ouvrage de référence {index}"
        document_kind = "book"
    elif source_type == "webliography":
        metadata_row["link"] = f"https://example.org/source-{index}"
        metadata_row["site"] = f"Site documentaire {index}"
        metadata_row["page"] = f"Page documentaire {index}"
        document_kind = "other"
    else:
        metadata_row["link"] = f"https://example.org/video-{index}"
        metadata_row["title"] = f"Vidéo documentaire {index}"
        metadata_row["site"] = f"Plateforme vidéo {index}"
        document_kind = "other"
    return {
        "id": source_id,
        "type": source_type,
        "language": "fr",
        "metadata": metadata_row,
        "verification": {
            "status": "verified",
            "verified_at": "2026-08-03T20:30:00+02:00",
            "primary_source": False,
            "notes": ["Notice et langue vérifiées pour la revue française."],
            "language_verified": True,
            "authorship_checked": True,
            "authorship_verified": True,
            "authorship_rechecked_after_site_match": False,
            "authorship_recheck_notes": [],
        },
        "usage": usages,
        "deduplication_key": f"source-{index}",
        "document_kind": document_kind,
        "equivalence_group": None,
    }


def complete_content_review(workspace: Path) -> None:
    review_path = workspace / "reviews/fr/content_review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    debate = review["debate"]["review"]
    debate.update({
        "status": "approved",
        "subject_decision": "change",
        "proposed_subject": "Débat test",
        "complete_topic_decision": "change",
        "proposed_complete_topic": "la proposition du débat test",
        "topic_label_rationale": "Le libellé nominal désigne directement la controverse sans reprendre une question.",
        "common_acronym": None,
        "complete_topic_initial_capital_justification": None,
        "introduction_decision": "change",
        "proposed_introduction": "{{Sous-partie|titre=Définition et périmètre|contenu=La proposition du débat test oppose deux réponses clairement délimitées et précise ce qui est effectivement discuté.}}{{Sous-partie|titre=Enjeux du débat|contenu=La réponse retenue modifie la manière d’expliquer le phénomène étudié et les critères utilisés pour accepter une conclusion. Elle peut aussi orienter des décisions collectives, des pratiques institutionnelles et des choix individuels qui dépassent la seule formulation théorique. Une suspension du jugement déplace enfin l’attention vers les limites des preuves disponibles et vers le degré de confiance raisonnablement accordé à chaque position.}}",
        "introduction_rationale": "Cette introduction définit le sujet et développe des conséquences concrètes sans recopier le graphe argumentatif.",
        "subsections": [{
            "title": "Définition et périmètre",
            "purpose": "Définir la proposition et préciser le périmètre nécessaire à la compréhension du désaccord.",
            "necessary_for_understanding": True,
            "technical_or_specialized": False,
            "relevance_to_debate_explained": True,
            "stakes_section": False,
            "concrete_stakes": [],
        }, {
            "title": "Enjeux du débat",
            "purpose": "Expliquer les conséquences intellectuelles, institutionnelles et pratiques des réponses possibles.",
            "necessary_for_understanding": True,
            "technical_or_specialized": False,
            "relevance_to_debate_explained": True,
            "stakes_section": True,
            "concrete_stakes": [
                "Modification des cadres explicatifs et des critères de rationalité", 
                "Conséquences sur les décisions collectives et les pratiques institutionnelles"
            ],
        }],
        "specialized_term_inventory": [
            {
                "subsection_title": "Définition et périmètre",
                "scan_complete": True,
                "scan_note": "La sous-partie a été relue intégralement et ne contient aucune notion spécialisée exigeant un lien ou une définition supplémentaire.",
                "terms": [],
            },
            {
                "subsection_title": "Enjeux du débat",
                "scan_complete": True,
                "scan_note": "La sous-partie a été relue intégralement et son vocabulaire reste suffisamment explicite pour un lecteur non spécialiste.",
                "terms": [],
            },
        ],
        "wikipedia_articles_decision": "change",
        "proposed_wikipedia_articles": ["Argumentation"],
        "wikipedia_articles_verified": True,
        "documentation_decisions": {bucket: "change" for bucket in content.DEBATE_BUCKETS},
        "documentation_rationales": {bucket: "Ces deux références documentent spécifiquement la position et la famille concernées." for bucket in content.DEBATE_BUCKETS},
        "documentation_family_notes": {
            "bibliography": "Deux ouvrages de synthèse français couvrent chaque position et le cadrage général.",
            "webliography": "Deux ressources web françaises vérifiées complètent chaque position et le contexte.",
            "videography": "Deux ressources vidéo françaises vérifiées présentent chaque position et la synthèse.",
        },
        "reviewer": "Relecteur Wikidéb'IA",
        "reviewed_at": "2026-08-03T21:00:00+02:00",
        "note": "La page Débat française est prête pour le verrouillage du contenu.",
    })
    for field in content.INTRO_TRUE_FIELDS:
        debate[field] = True
    debate["proposed_documentation"] = {
        "bibliographie-pour": ["S00001"],
        "bibliographie-contre": ["S00002"],
        "bibliographie-ni-pour-ni-contre": [],
        "sitographie-pour": ["S00003"],
        "sitographie-contre": ["S00004"],
        "sitographie-ni-pour-ni-contre": [],
        "vidéographie-pour": ["S00005"],
        "vidéographie-contre": ["S00006"],
        "vidéographie-ni-pour-ni-contre": [],
    }
    for index, item in enumerate(review["arguments"], start=1):
        node_id = item["id"]
        label = ("première", "deuxième", "troisième", "quatrième")[index - 1]
        expression = f"La {label} preuve donne au débat une base nettement plus solide"
        summary = (
            f"{expression} en reliant une prémisse explicite à la conclusion propre au nœud {node_id}. "
            "Le mécanisme est présenté dans un langage accessible, sans anticiper l'objection qui lui sera opposée."
        )
        decision = item["review"]
        decision.update({
            "status": "approved",
            "summary_decision": "change",
            "proposed_summary": summary,
            "summary_rationale": "Le texte développe les prémisses, le mécanisme et la conclusion propres à ce nœud.",
            "documentation_decisions": {bucket: "change" for bucket in content.ARGUMENT_BUCKETS},
            "proposed_sources": {"bibliography": ["S00001"], "webliography": [], "videography": []},
            "documentation_rationale": "La référence retenue soutient le cœur du résumé sans imposer de quota artificiel.",
            "forceful_expression": expression,
            "quantitative_claims_verified": False,
            "quantitative_claims_note": "Aucune affirmation quantitative n’est présente dans ce résumé.",
            "reviewer": "Relecteur Wikidéb'IA",
            "reviewed_at": "2026-08-03T21:00:00+02:00",
            "note": "Résumé français relu pour la fidélité logique, l’accessibilité et la force expressive.",
        })
        for field in content.SUMMARY_TRUE_FIELDS:
            decision[field] = True
    review["global_review"] = {
        "reviewer": "Relecteur Wikidéb'IA",
        "reviewed_at": "2026-08-03T21:15:00+02:00",
        "all_french_content_reviewed": True,
        "all_selected_sources_verified": True,
        "no_final_pages_generated": True,
        "english_translation_not_started": True,
        "blocking_issues": [],
        "note": "Toutes les décisions françaises de contenu et de documentation ont été relues.",
    }
    common.write_json(review_path, review)

    source_roles = {
        "S00001": "pro_reference", "S00002": "con_reference",
        "S00003": "pro_reference", "S00004": "con_reference",
        "S00005": "pro_reference", "S00006": "con_reference",
    }
    sources = []
    for source_id, source_type in (("S00001", "bibliography"), ("S00002", "bibliography"), ("S00003", "webliography"), ("S00004", "webliography"), ("S00005", "videography"), ("S00006", "videography")):
        usages = [{
            "page_id": "debat_test",
            "language": "fr",
            "role": source_roles[source_id],
            "language_fit": "native",
            "preferred_equivalent_source_id": None,
            "documentary_scope": "broad_synthesis",
            "selection_reason": "Cette source française documente précisément l’orientation qui lui est attribuée.",
        }]
        if source_id == "S00001":
            usages.extend({
                "page_id": item["id"],
                "language": "fr",
                "role": "supports_summary",
                "argument_development_verified": True,
                "also_develops_objections": False,
                "objection_coverage_note": None,
                "language_fit": "native",
                "preferred_equivalent_source_id": None,
                "documentary_scope": "narrow_argument",
                "selection_reason": "Cette source soutient directement le mécanisme exposé dans le résumé de l'argument.",
            } for item in review["arguments"])
        sources.append(source_row(source_id, source_type, usages))
    working = {
        "schema": content.SOURCES_WORKING_SCHEMA,
        "source_registry_version": "1.0",
        "debate_id": "debat_test",
        "work_id": review["work_id"],
        "status": "draft",
        "prepared_at": review["prepared_at"],
        "sources": sources,
    }
    common.write_json(workspace / "data/sources_working.json", working)


def test_prepare_content_review_is_read_only_for_reviewed_copy(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    before = common.full_tree_sha256(workspace / "reviewed-copy")
    result = content.prepare_review(project, "debat_test", work_id)
    assert result["status"] == "fr_content_review_ready"
    assert common.full_tree_sha256(workspace / "reviewed-copy") == before
    review = json.loads((workspace / "reviews/fr/content_review.json").read_text(encoding="utf-8"))
    assert len(review["arguments"]) == 4
    assert review["debate"]["source"]["introduction"] == ""
    citations = {item["id"]: item["source"]["citations"] for item in review["arguments"]}
    assert citations["A0001"][0]["avertissements-citation"] == "Texte abrégé"
    assert citations["A0001"][0]["preserved_parameters"][0]["name"] == "auteurs"
    assert citations["A0002"][0]["date"] == "juin 2012"
    assert citations["A0004"][0]["date"] == "1971"
    translation = json.loads((workspace / "reviews/en/translation_readiness.json").read_text(encoding="utf-8"))
    assert translation["status"] == "blocked_by_french_content_review"


def test_finalize_content_review_seals_sources_and_content(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    before = common.full_tree_sha256(workspace / "reviewed-copy")
    result = content.finalize_review(project, "debat_test", work_id)
    assert result["status"] == "fr_content_review_finalized"
    assert result["sources"] == 6
    assert result["arguments"] == 4
    assert common.full_tree_sha256(workspace / "reviewed-copy") == before
    sealed = json.loads((workspace / "reviews/fr/content_review.json").read_text(encoding="utf-8"))
    assert sealed["review_sha256"] == content.content_review_sha256(sealed)
    assert sealed["summary"]["debate_documentary_references"] == 6
    assert sealed["summary"]["citations"] == 4


def test_finalize_accepts_single_reference_in_a_debate_bucket(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    result = content.finalize_review(project, "debat_test", work_id)
    assert result["status"] == "fr_content_review_finalized"


def test_finalize_rejects_same_reference_in_pro_and_con_buckets(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    review_path = workspace / "reviews/fr/content_review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["debate"]["review"]["proposed_documentation"]["bibliographie-contre"] = ["S00001"]
    common.write_json(review_path, review)
    sources_path = workspace / "data/sources_working.json"
    sources = json.loads(sources_path.read_text(encoding="utf-8"))
    source = next(row for row in sources["sources"] if row["id"] == "S00001")
    source["usage"].append({
        "page_id": "debat_test", "language": "fr", "role": "con_reference",
        "language_fit": "native", "preferred_equivalent_source_id": None,
        "documentary_scope": "broad_synthesis",
        "selection_reason": "Cette attribution contradictoire sert uniquement à vérifier le blocage automatique.",
    })
    common.write_json(sources_path, sources)
    try:
        content.finalize_review(project, "debat_test", work_id)
    except content.ContentReviewError as exc:
        assert "ni pour ni contre" in str(exc) or "plusieurs orientations" in str(exc)
    else:
        raise AssertionError("Référence dupliquée entre pour et contre acceptée")


def test_finalize_rejects_forceful_expression_not_in_summary(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    path = workspace / "reviews/fr/content_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["arguments"][0]["review"]["forceful_expression"] = "Une formule absente du texte final"
    common.write_json(path, data)
    try:
        content.finalize_review(project, "debat_test", work_id)
    except content.ContentReviewError as exc:
        assert "expression de force" in str(exc)
    else:
        raise AssertionError("Expression absente acceptée")


def test_finalize_rejects_unverified_source(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    path = workspace / "data/sources_working.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["sources"][0]["verification"]["status"] = "unverified"
    common.write_json(path, data)
    try:
        content.finalize_review(project, "debat_test", work_id)
    except content.ContentReviewError as exc:
        assert "non vérifiée" in str(exc)
    else:
        raise AssertionError("Source non vérifiée acceptée")


def test_apply_content_review_creates_distinct_copy(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    finalized = content.finalize_review(project, "debat_test", work_id)
    corpus_hash = common.full_tree_sha256(project / "corpus/debat_test")
    working_hash = common.full_tree_sha256(workspace / "working-copy")
    reviewed_hash = common.full_tree_sha256(workspace / "reviewed-copy")
    metadata_lock = (workspace / "reviewed-copy/data/fr_page_metadata_lock.json").read_bytes()
    result = content.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    target = workspace / "content-reviewed-copy"
    assert result["status"] == "fr_content_applied"
    assert target.is_dir()
    assert common.full_tree_sha256(project / "corpus/debat_test") == corpus_hash
    assert common.full_tree_sha256(workspace / "working-copy") == working_hash
    assert common.full_tree_sha256(workspace / "reviewed-copy") == reviewed_hash
    assert (target / "data/fr_page_metadata_lock.json").read_bytes() == metadata_lock
    assert not (target / "output").exists()
    lock = json.loads((target / "data/fr_content_lock.json").read_text(encoding="utf-8"))
    assert lock["status"] == "locked_for_translation_and_generation"
    assert len(lock["arguments"]) == 4
    sources = json.loads((target / "data/sources.json").read_text(encoding="utf-8"))
    assert len(sources["sources"]) == 6
    translation = json.loads((workspace / "reviews/en/translation_readiness.json").read_text(encoding="utf-8"))
    assert translation["status"] == "ready_for_translation"


def test_apply_requires_exact_review_hash(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    content.finalize_review(project, "debat_test", work_id)
    try:
        content.apply_review(project, "debat_test", work_id, "0" * 64)
    except content.ContentReviewError as exc:
        assert "empreinte confirmée" in str(exc)
    else:
        raise AssertionError("Mauvaise empreinte acceptée")
    assert not (workspace / "content-reviewed-copy").exists()


def test_finalize_rejects_reviewed_copy_changed_after_prepare(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    (workspace / "reviewed-copy/scope.json").write_text("{}\n", encoding="utf-8")
    try:
        content.finalize_review(project, "debat_test", work_id)
    except content.ContentReviewError as exc:
        assert "reviewed-copy" in str(exc)
    else:
        raise AssertionError("Copie révisée altérée acceptée")


def test_finalize_rejects_youtube_video_without_creator(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    sources_path = workspace / "data/sources_working.json"
    data = json.loads(sources_path.read_text(encoding="utf-8"))
    video = next(row for row in data["sources"] if row["id"] == "S00005")
    video["metadata"]["link"] = "https://www.youtube.com/watch?v=example"
    video["metadata"]["authors"] = []
    common.write_json(sources_path, data)
    try:
        content.finalize_review(project, "debat_test", work_id)
    except content.ContentReviewError as exc:
        assert "créateur ou la chaîne" in str(exc)
    else:
        raise AssertionError("Vidéo YouTube sans créateur acceptée")


def test_finalize_rejects_missing_mandatory_stakes_subsection(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    review_path = workspace / "reviews/fr/content_review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    debate = review["debate"]["review"]
    debate["proposed_introduction"] = "{{Sous-partie|titre=Définition et périmètre|contenu=Une introduction suffisamment développée mais privée de la rubrique obligatoire consacrée aux conséquences du désaccord.}}"
    debate["subsections"] = [debate["subsections"][0]]
    common.write_json(review_path, review)
    try:
        content.finalize_review(project, "debat_test", work_id)
    except content.ContentReviewError as exc:
        assert "Enjeux du débat" in str(exc)
    else:
        raise AssertionError("La rubrique Enjeux du débat manquante aurait dû être refusée")


def test_finalize_rejects_symbolic_stakes_subsection(tmp_path: Path):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    review_path = workspace / "reviews/fr/content_review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    debate = review["debate"]["review"]
    debate["proposed_introduction"] = "{{Sous-partie|titre=Définition et périmètre|contenu=Le périmètre du débat est défini.}}{{Sous-partie|titre=Enjeux du débat|contenu=Ce débat présente des enjeux philosophiques, sociaux et politiques importants.}}"
    common.write_json(review_path, review)
    try:
        content.finalize_review(project, "debat_test", work_id)
    except content.ContentReviewError as exc:
        assert "trop brève ou symbolique" in str(exc)
    else:
        raise AssertionError("Une rubrique d’enjeux purement symbolique aurait dû être refusée")



def test_specialized_term_inventory_covers_links_and_prior_treatment():
    from wikidebia_content_review import _validated_specialized_term_inventory
    intro = "{{Sous-partie|titre=Définition|contenu=Un {{Lien Wikipédia|article=Nécessité|texte-affiché=principe nécessaire}} est distingué.}}{{Sous-partie|titre=Suite|contenu=Le principe nécessaire est repris.}}"
    ledger=[{"title":"Définition","technical_or_specialized":True},{"title":"Suite","technical_or_specialized":True}]
    inventory=[{"subsection_title":"Définition","scan_complete":True,"scan_note":"La sous-partie entière a été relue pour identifier toutes les notions spécialisées.","terms":[{"term":"principe nécessaire","treatment":"wikipedia_link","article":"Nécessité"}]},{"subsection_title":"Suite","scan_complete":True,"scan_note":"La sous-partie entière a été relue et la répétition renvoie au premier traitement.","terms":[{"term":"principe nécessaire","treatment":"prior_treatment","prior_subsection_title":"Définition","prior_term":"principe nécessaire"}]}]
    assert _validated_specialized_term_inventory(intro,inventory,ledger)[1]['terms'][0]['treatment']=='prior_treatment'


def test_specialized_term_inventory_rejects_undeclared_link():
    from wikidebia_content_review import _validated_specialized_term_inventory, ContentReviewError
    intro = "{{Sous-partie|titre=Définition|contenu=Un {{Lien Wikipédia|article=Nécessité|texte-affiché=principe nécessaire}} est distingué.}}"
    ledger=[{"title":"Définition","technical_or_specialized":True}]
    inventory=[{"subsection_title":"Définition","scan_complete":True,"scan_note":"La sous-partie entière a été relue pour identifier toutes les notions spécialisées.","terms":[{"term":"principe nécessaire","treatment":"context_sufficient","justification":"Le contexte donne une définition complète de cette notion dans la phrase."}]}]
    try:
        _validated_specialized_term_inventory(intro,inventory,ledger)
    except ContentReviewError:
        return
    raise AssertionError('le lien non déclaré devait être refusé')


def test_argument_established_name_parameters_are_preserved_import_parameters():
    assert 'nom-consacré' in content.PAGE_LIFECYCLE_PARAMETERS['argument']
    assert 'nom' in content.PAGE_LIFECYCLE_PARAMETERS['argument']

# Historical test-name alias retained for non-regression traceability.
def test_argument_name_is_a_preserved_import_parameter():
    assert 'nom' in content.PAGE_LIFECYCLE_PARAMETERS['argument']
