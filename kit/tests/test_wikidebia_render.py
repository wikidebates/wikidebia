from __future__ import annotations

import importlib.util
import json
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


render = load_module("wikidebia_render")
translation = sys.modules.get("wikidebia_translation_review") or load_module("wikidebia_translation_review")
common = sys.modules["wikidebia_corpus_build"]


def fake_validator(*args, **kwargs):
    return {"validator_version": "0.4.29", "result": "passed", "summary": {"errors": 0, "warnings": 0}}


render._run_validator = fake_validator
from test_wikidebia_translation_review import make_french_locked, complete_translation_review  # noqa: E402


def make_translated(tmp_path: Path) -> tuple[Path, Path, str, str]:
    project, workspace, work_id = make_french_locked(tmp_path)
    norm_path = project / "norms/normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.57.md"
    norm_path.parent.mkdir(parents=True, exist_ok=True)
    norm_path.write_text("# Norme de test 1.2.27\n", encoding="utf-8")
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    sealed = translation.finalize_review(project, "debat_test", work_id)
    translation.apply_review(project, "debat_test", work_id, sealed["review_sha256"])
    translated = workspace / "translated-copy"
    registry = json.loads((translated / "data/registre_debat.json").read_text(encoding="utf-8"))
    edges = {row["id"]: row for row in registry["graph"]["edges"]}
    entries = []
    for occurrence in registry["graph"]["occurrences"]:
        depth = occurrence["depth"]
        entry = {
            "occurrence_id": occurrence["id"],
            "node_id": occurrence["node_id"],
            "declared_depth": depth,
            "placement_status": "approved",
            "direct_fit": True,
            "rationale": "Le placement a été relu formellement et correspond à la cible logique immédiate du raisonnement.",
        }
        if depth == 1:
            entry.update({
                "declared_function": "main_argument",
                "semantic_target": "debate",
                "main_argument_review": {
                    "direct_answer_to_debate": True,
                    "autonomous_without_parent": True,
                    "organizes_distinct_argument_family": True,
                    "more_general_nonduplicate_parent_available": False,
                    "principally_supports_or_attacks_specific_argument": False,
                    "principally_example_or_specialization": False,
                },
            })
        else:
            entry.update({
                "declared_function": edges[occurrence["edge_id"]]["relation"],
                "semantic_target": occurrence["parent_occurrence_id"],
                "subordinate_review": {
                    "parent_is_best_immediate_target": True,
                    "relation_to_parent_explicit": True,
                },
            })
        entries.append(entry)
    (translated / "reviews/graph_placement_review.json").write_text(json.dumps({
        "normative_revision": "1.2.27",
        "debate_id": "debat_test",
        "status": "approved",
        "entries": entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    meta_path = workspace / "workspace.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["translated_copy"]["tree_sha256"] = common.full_tree_sha256(translated)
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = sys.modules["wikidebia_editorial_workspace"].workspace_receipt_hash(meta)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return project, workspace, work_id, sealed["review_sha256"]


def test_render_creates_distinct_bilingual_pages_and_direct_interlanguage_links(tmp_path: Path):
    project, workspace, work_id, review_sha = make_translated(tmp_path)
    translated_before = common.full_tree_sha256(workspace / "translated-copy")
    result = render.render_workspace(project, "debat_test", work_id, review_sha)
    target = workspace / "rendered-copy"
    assert result["status"] == "bilingual_rendered"
    assert result["pages"] == 10
    assert result["french_interlanguage_links"] == 5
    assert result["english_interlanguage_links"] == 0
    assert common.full_tree_sha256(workspace / "translated-copy") == translated_before
    registry = json.loads((target / "data/registre_debat.json").read_text(encoding="utf-8"))
    fr_debate = (target / "output/fr/debate/debate.wiki").read_text(encoding="utf-8")
    en_title = registry["debate"]["pages"]["en"]["canonical_title"]
    assert f"{{{{Lien interlangue\n|langue=en\n|page={en_title}\n}}}}" in fr_debate
    for node in registry["graph"]["nodes"]:
        if node["status"] != "active":
            continue
        fr = (target / f"output/fr/arguments/{node['id']}.wiki").read_text(encoding="utf-8")
        assert f"{{{{Lien interlangue\n|langue=en\n|page={node['en']['canonical_title']}\n}}}}" in fr
    for path in (target / "output/en").rglob("*.wiki"):
        assert "Lien interlangue" not in path.read_text(encoding="utf-8")
        assert "|interlangue=" not in path.read_text(encoding="utf-8")


def test_render_emits_translated_citations_without_mutating_source_metadata(tmp_path: Path):
    project, workspace, work_id, review_sha = make_translated(tmp_path)
    render.render_workspace(project, "debat_test", work_id, review_sha)
    target = workspace / "rendered-copy"
    fr = (target / "output/fr/arguments/A0001.wiki").read_text(encoding="utf-8")
    en = (target / "output/en/arguments/A0001.wiki").read_text(encoding="utf-8")
    assert "|citation=La liberté consiste à vouloir ce que l'on veut." in fr
    assert "|date=25 juin 2012" in fr
    assert "|quote=Freedom consists in wanting what one wants." in en
    assert "|date=25 June 2012" in en
    assert "|authors=Harry G. Frankfurt" in en
    assert "|article=Freedom of the Will and the Concept of a Person" in en
    assert "|work=The Importance of What We Care About" in en
    assert "|warnings=Texte abrégé, AI-translated quote" in en
    for forbidden in ("|citation=", "|auteurs=", "|ouvrage=", "|numéro=", "|localisation=", "|édition=", "|lieu=", "|lien=", "|avertissements-citation="):
        assert forbidden not in en
    assert "|quotes={{Quote" in en
    assert "|quotes={{Citation" not in en
    assert "|citations={{Citation" in fr


def test_render_requires_exact_translation_hash(tmp_path: Path):
    project, workspace, work_id, _ = make_translated(tmp_path)
    try:
        render.render_workspace(project, "debat_test", work_id, "0" * 64)
    except render.RenderError as exc:
        assert "empreinte confirmée" in str(exc)
    else:
        raise AssertionError("Une empreinte de traduction erronée a été acceptée")
    assert not (workspace / "rendered-copy").exists()


def test_render_is_idempotent_and_locks_graph(tmp_path: Path):
    project, workspace, work_id, review_sha = make_translated(tmp_path)
    first = render.render_workspace(project, "debat_test", work_id, review_sha)
    second = render.render_workspace(project, "debat_test", work_id, review_sha)
    assert second["idempotent"] is True
    assert second["rendered_copy_tree_sha256"] == first["rendered_copy_tree_sha256"]
    target = workspace / "rendered-copy"
    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    registry = json.loads((target / "data/registre_debat.json").read_text(encoding="utf-8"))
    assert manifest["global_status"] == "bilingual_validated"
    assert registry["graph"]["lifecycle"]["status"] == "locked"
    assert all(page["status"] == "validated" for page in manifest["pages"])
    assert not any(path.name.endswith(".wiki") for path in (workspace / "translated-copy").rglob("*.wiki") if "imports" not in path.parts)


def test_render_lifecycle_fields_depend_on_page_origin():
    registry={
        'debate': {'pages': {'en': {'canonical_title':'Topic'}}},
        'graph': {'occurrences': [], 'nodes': [], 'edges': []},
    }
    metadata={'debate': {'rubriques':['Société'], 'keywords':['sujet']}}
    existing={
        'debate': {
            'subject':'Sujet','complete_topic':'la question du sujet','introduction':'Texte.',
            'wikipedia_articles':[],'documentation':{},
            'page_origin':'preexisting',
            'preserved_parameters':{
                'avancement':{'present':True,'value':'Débat en construction'},
                'avertissements-débat':{'present':False,'value':None},
                'débats-connexes':{'present':True,'value':'{{Débat connexe|page=Autre débat}}'},
            },
        }
    }
    text=render._render_debate(lang='fr',registry=registry,metadata_lock=metadata,content_lock=existing,sources={},creation_date='2026-08-05')
    assert '|avancement=Débat en construction' in text
    assert '|avertissements-débat=' not in text
    assert '|débats-connexes={{Débat connexe|page=Autre débat}}' in text
    new={'debate': {**existing['debate'],'page_origin':'new','preserved_parameters':{}}}
    text=render._render_debate(lang='fr',registry=registry,metadata_lock=metadata,content_lock=new,sources={},creation_date='2026-08-05')
    assert '|avancement=Débat construit' in text
    assert '|avertissements-débat=Débat généré par IA' in text
    assert '|débats-connexes=' not in text


def test_render_existing_argument_preserves_absent_ai_warning():
    node={'id':'A0001','fr':{'rubriques':['Société'],'keywords':['sujet']},'en':{'canonical_title':'Argument topic'}}
    registry={'graph':{'edges':[],'occurrences':[],'nodes':[node]}}
    content={
        'summary':'Le raisonnement est développé sans modifier les paramètres historiques.',
        'citations':[],'sources':{},'page_origin':'preexisting',
        'preserved_parameters':{'avertissements-argument':{'present':False,'value':None}},
    }
    text=render._render_argument(lang='fr',node=node,content=content,registry=registry,sources={},creation_date='2026-08-05')
    assert '|avertissements-argument=' not in text


def test_render_preserves_detailed_debate_and_omits_local_relations():
    child={'id':'A0002','fr':{'canonical_title':'Argument enfant','displayed_title':'Argument enfant','rubriques':['Société'],'keywords':['sujet']}}
    node={'id':'A0001','fr':{'rubriques':['Société'],'keywords':['sujet']},'en':{'canonical_title':'Argument topic'}}
    registry={'graph':{'edges':[{'id':'E00001','parent_node_id':'A0001','child_node_id':'A0002','relation':'justification','order':1,'status':'active'}],'occurrences':[],'nodes':[node,child]}}
    content={
        'summary':'Le raisonnement renvoie vers un débat autonome qui porte le développement détaillé.',
        'citations':[],'sources':{},'page_origin':'preexisting',
        'preserved_parameters':{
            'avertissements-argument':{'present':False,'value':None},
            'débat-détaillé':{'present':True,'value':'Débat sous-jacent'},
        },
    }
    text=render._render_argument(lang='fr',node=node,content=content,registry=registry,sources={},creation_date='2026-08-05')
    assert '|débat-détaillé=Débat sous-jacent' in text
    assert '|justifications=' not in text
    assert '|objections=' not in text


def test_render_preserves_historical_argument_name():
    node={'id':'A0001','fr':{'rubriques':['Philosophie'],'keywords':['Dieu']},'en':{'canonical_title':'Argument topic'}}
    registry={'graph':{'edges':[],'occurrences':[],'nodes':[node]}}
    content={
        'summary':'Résumé historique conservé.', 'citations':[], 'sources':{}, 'page_origin':'preexisting',
        'preserved_parameters':{
            'nom':{'present':True,'value':'Argument cosmologique'},
            'avertissements-argument':{'present':False,'value':None},
        },
    }
    text=render._render_argument(lang='fr',node=node,content=content,registry=registry,sources={},creation_date='2026-08-05')
    assert '|nom=Argument cosmologique' in text
    assert text.index('|nom=') < text.index('|résumé=')
