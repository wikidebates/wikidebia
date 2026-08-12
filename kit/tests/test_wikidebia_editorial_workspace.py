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


workspace = load_module("wikidebia_editorial_workspace")
common = sys.modules["wikidebia_corpus_build"]

init = load_module("wikidebia_corpus_init")
from test_wikidebia_corpus_init import make_extraction  # noqa: E402


def make_draft_project(tmp_path: Path) -> tuple[Path, Path]:
    project = tmp_path / "project"
    (project / "corpus").mkdir(parents=True)
    source = make_extraction(tmp_path / "source")
    corpus = project / "corpus" / "debat_test"
    init.build_corpus(source, corpus, debate_id="debat_test", short_code="TEST", scope_summary=None, overwrite=False)
    return project, corpus


def make_promoted_project(tmp_path: Path) -> tuple[Path, Path]:
    project, corpus = make_draft_project(tmp_path)
    manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
    registry = json.loads((corpus / "data/registre_debat.json").read_text(encoding="utf-8"))
    projection = json.loads((corpus / "graph/graphe_argumentatif.json").read_text(encoding="utf-8"))
    structural = common.structural_sha256(registry)
    manifest["global_status"] = "graph_validated"
    registry["graph"]["lifecycle"].update({
        "status": "validated",
        "validated_at": "2026-08-03T19:00:00+00:00",
        "structural_sha256": structural,
    })
    projection["lifecycle"] = dict(registry["graph"]["lifecycle"])
    common.write_json(corpus / "manifest.json", manifest)
    common.write_json(corpus / "data/registre_debat.json", registry)
    common.write_json(corpus / "graph/graphe_argumentatif.json", projection)
    return project, corpus


def test_workspace_init_preserves_source_and_creates_complete_working_copy(tmp_path: Path):
    project, source = make_promoted_project(tmp_path)
    source_hash = common.full_tree_sha256(source)
    result = workspace.create_workspace(project, "debat_test", "EDIT-TEST-001")
    target = project / result["workspace"]
    assert result["status"] == "audit_ready"
    assert common.full_tree_sha256(source) == source_hash
    assert common.full_tree_sha256(target / "working-copy") == source_hash
    assert (target / "workspace.json").is_file()
    assert (target / "audits/editorial_inventory.json").is_file()
    assert (target / "reviews/fr/page_metadata_review.json").is_file()
    assert (target / "reviews/en/translation_readiness.json").is_file()
    assert (target / "tasks/editorial_tasks.json").is_file()
    assert (target / "data/keyword_vocabulary_working.json").is_file()
    assert (target / "changes/changeset.json").is_file()
    assert not (target / "working-copy/output").exists()


def test_workspace_audit_opens_metadata_tasks_without_applying_corrections(tmp_path: Path):
    project, _ = make_promoted_project(tmp_path)
    result = workspace.create_workspace(project, "debat_test", "EDIT-TEST-002")
    target = project / result["workspace"]
    audit = json.loads((target / "audits/editorial_inventory.json").read_text(encoding="utf-8"))
    codes = {issue["code"] for item in audit["items"] for issue in item["diagnostics"]}
    corpus_codes = {issue["code"] for issue in audit["corpus_diagnostics"]}
    assert "KEYWORDS_TOO_FEW" in codes
    assert "DOMINANT_EXACT_KEYWORD_SET_OVER_25_PERCENT" in corpus_codes
    assert audit["scope"]["automatic_corrections_applied"] is False
    assert audit["scope"]["final_pages_generated"] is False
    review_ledger = json.loads((target / "reviews/fr/page_metadata_review.json").read_text(encoding="utf-8"))
    assert {item["review"]["status"] for item in review_ledger["items"]} == {"pending"}
    changeset = json.loads((target / "changes/changeset.json").read_text(encoding="utf-8"))
    assert changeset["status"] == "empty"
    assert changeset["operations"] == []


def test_workspace_translation_is_explicitly_blocked_until_french_review(tmp_path: Path):
    project, _ = make_promoted_project(tmp_path)
    result = workspace.create_workspace(project, "debat_test", "EDIT-TEST-003")
    target = project / result["workspace"]
    translation = json.loads((target / "reviews/en/translation_readiness.json").read_text(encoding="utf-8"))
    assert translation["source_language"] == "fr"
    assert translation["target_language"] == "en"
    assert {item["translation_status"] for item in translation["items"]} == {"blocked_by_french_review"}
    meta = json.loads((target / "workspace.json").read_text(encoding="utf-8"))
    assert meta["boundaries"]["english_translation_started"] is False


def test_workspace_refuses_existing_work_id(tmp_path: Path):
    project, _ = make_promoted_project(tmp_path)
    workspace.create_workspace(project, "debat_test", "EDIT-TEST-004")
    try:
        workspace.create_workspace(project, "debat_test", "EDIT-TEST-004")
    except workspace.WorkspaceError as exc:
        assert "existe déjà" in str(exc)
    else:
        raise AssertionError("workspace existant remplacé")


def test_workspace_refuses_graph_draft_masquerading_as_active_corpus(tmp_path: Path):
    project, target = make_draft_project(tmp_path)
    try:
        workspace.create_workspace(project, "debat_test", "EDIT-TEST-005")
    except common.CorpusBuildError as exc:
        assert "graph_validated" in str(exc)
    else:
        raise AssertionError("corpus graph_draft accepté")


def test_workspace_refuses_symlink_inside_promoted_corpus(tmp_path: Path):
    project, source = make_promoted_project(tmp_path)
    (source / "imports/fr/link").symlink_to(source / "manifest.json")
    try:
        workspace.create_workspace(project, "debat_test", "EDIT-TEST-006")
    except common.CorpusBuildError as exc:
        assert "Lien symbolique" in str(exc)
    else:
        raise AssertionError("lien symbolique accepté")


def test_auto_work_ids_are_monotonic_and_non_destructive(tmp_path: Path):
    project, _ = make_promoted_project(tmp_path)
    first = workspace.create_workspace(project, "debat_test")
    second = workspace.create_workspace(project, "debat_test")
    assert first["work_id"] != second["work_id"]
    assert first["work_id"] < second["work_id"]
    assert (project / first["workspace"]).is_dir()
    assert (project / second["workspace"]).is_dir()


def test_invalid_explicit_work_id_is_rejected(tmp_path: Path):
    project, _ = make_promoted_project(tmp_path)
    try:
        workspace.create_workspace(project, "debat_test", "mauvais id")
    except workspace.WorkspaceError as exc:
        assert "work_id invalide" in str(exc)
    else:
        raise AssertionError("work_id invalide accepté")


def test_rubrique_sort_uses_french_alphabetical_order_with_accents():
    values = ["Droit", "Économie", "Éthique", "Politique", "Société"]
    assert workspace.rubrique_diagnostics(values, False, enforce_creation_count=False) == []
