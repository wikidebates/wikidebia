from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import wikidebia_editorial_review as editorial
import wikidebia_content_review as content
import wikidebia_french_checkpoint as checkpoint
import wikidebia_review_workflow as workflow
from test_wikidebia_editorial_review import make_workspace, complete_review


def _title_applied(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    finalized = editorial.finalize_title_review(project, "debat_test", work_id)
    editorial.apply_title_review(project, "debat_test", work_id, finalized["review_sha256"])
    return project, workspace, work_id


def test_title_checkpoint_does_not_publish_classification_changes(tmp_path: Path):
    project, workspace, work_id = _title_applied(tmp_path)
    cp = checkpoint.build_checkpoint(project, "debat_test", work_id, stage="graph")
    text = (cp / "output/fr/arguments/A0001.wiki").read_text(encoding="utf-8")
    # complete_review proposed extra keywords, but the graph/title checkpoint
    # must preserve the imported classification verbatim.
    assert "|mots-clés=test" in text
    assert "preuve, raisonnement" not in text
    debate = (cp / "output/fr/debate/debate.wiki").read_text(encoding="utf-8")
    assert "La démonstration A soutient explicitement la proposition du débat test" in debate
    manifest = json.loads((cp / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["translation_status"]["en"] == "deferred"
    receipt = json.loads((project / ".state/fr-publication/debat_test" / work_id / "graph/checkpoint.json").read_text(encoding="utf-8"))
    assert receipt["stage"] == "graph"
    delta = json.loads((cp / "data/fr_graph_checkpoint_delta.json").read_text(encoding="utf-8"))
    assert delta["status"] == "passed"
    assert {row["page_id"] for row in delta["pages"]} == {"debat_test", "A0001", "A0002", "A0003", "A0004"}
    assert all(row["status"] == "verified" for row in delta["pages"])


def test_graph_checkpoint_omits_empty_relation_parameters(tmp_path: Path):
    project, _workspace, work_id = _title_applied(tmp_path)
    cp = checkpoint.build_checkpoint(project, "debat_test", work_id, stage="graph")

    for path in (cp / "output/fr/arguments").glob("*.wiki"):
        text = path.read_text(encoding="utf-8")
        assert "|justifications=\n" not in text
        assert "|objections=\n" not in text


def test_review_packages_split_titles_from_classification_and_content(tmp_path: Path):
    project, workspace, work_id = _title_applied(tmp_path)
    state = {
        "schema": workflow.WORKFLOW_SCHEMA, "schema_version": "1.0",
        "normative_revision": workflow.NORM_VERSION, "validator_version": workflow.VALIDATOR_VERSION,
        "kit_version": workflow.KIT_VERSION, "debate_id": "debat_test", "debate_title": "Débat test ?",
        "short_code": "TEST", "phase": "fr_metadata_review", "status": "running", "work_id": work_id,
        "pending_review": None, "created_at": "2026-08-12T10:00:00+02:00", "updated_at": "2026-08-12T10:00:00+02:00",
    }
    # Title package is deliberately title-only.
    title_pending = workflow._prepare_metadata_package(project, state)
    title_manifest = json.loads((project / title_pending["manifest_path"]).read_text(encoding="utf-8")) if title_pending.get("manifest_path") else None
    # Inspect the generated ZIP manifest through the pending state payload.
    import zipfile
    with zipfile.ZipFile(project / title_pending["package_path"]) as z:
        names = set(z.namelist())
        assert "editable/reviews/fr/page_metadata_review.json" in names
        assert "editable/data/keyword_vocabulary_working.json" not in names

    # Reset pending so the next package can be prepared in the same fixture.
    state["pending_review"] = None
    content.prepare_review(project, "debat_test", work_id)
    with open(workspace / "reviews/fr/classification_review.json", encoding="utf-8") as f:
        classification = json.load(f)
    assert classification["review_scope"] == "classification_and_content"
    pending = workflow.create_review_package(
        project, state, review_type="fr_content_review", base=workspace,
        editable_paths=["reviews/fr/content_review.json", "data/sources_working.json", "reviews/fr/classification_review.json", "data/keyword_vocabulary_working.json"],
        context_paths=["reviewed-copy/data/fr_page_metadata_lock.json"],
    )
    with zipfile.ZipFile(project / pending["package_path"]) as z:
        names = set(z.namelist())
        assert "editable/reviews/fr/classification_review.json" in names
        assert "editable/data/keyword_vocabulary_working.json" in names
        assert "editable/reviews/fr/content_review.json" in names
        assert "editable/data/sources_working.json" in names


def test_content_checkpoint_uses_published_graph_state_not_import_inventory(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    cp = project / "cp"; cp.mkdir()
    # _config is sufficient to assert the state-resolution contract: graph gets
    # an explicit import inventory; content deliberately omits it so StateResolver
    # resolves .state/published from checkpoint 1.
    inv = project / "inventory"; inv.mkdir()
    graph_cfg = checkpoint._config(project, "demo", "EDIT-1", cp, "graph", inv)
    content_cfg = checkpoint._config(project, "demo", "EDIT-1", cp, "content", None)
    g = json.loads(graph_cfg.read_text(encoding="utf-8"))
    c = json.loads(content_cfg.read_text(encoding="utf-8"))
    assert g["state_inventory_root"] == str(inv)
    assert "state_inventory_root" not in c
    assert c["published_state_dir"].endswith("/.state/published")
    assert g["validator"]["profile"] == checkpoint.GRAPH_VALIDATION_PROFILE
    assert g["validator"]["scopes"] == list(checkpoint.GRAPH_VALIDATION_SCOPES)
    assert "wikicode" not in g["validator"]["scopes"]
    assert c["validator"]["profile"] == checkpoint.CONTENT_VALIDATION_PROFILE
    assert "wikicode" in c["validator"]["scopes"]


def test_graph_checkpoint_uses_differential_validation_until_content_is_complete(tmp_path: Path):
    project, _workspace, work_id = _title_applied(tmp_path)
    cp = checkpoint.build_checkpoint(project, "debat_test", work_id, stage="graph")
    graph_config_path = checkpoint._config(project, "debat_test", work_id, cp, "graph", tmp_path / "inventory")
    graph_config = json.loads(graph_config_path.read_text(encoding="utf-8"))

    def validate(config):
        command = list(config["validator"]["command"])
        command.insert(command.index("validate") + 1, str(cp))
        for scope in config["validator"]["scopes"]:
            command.extend(["--scope", scope])
        command.extend(["--format", "json"])
        return subprocess.run(command, cwd=project, text=True, capture_output=True, check=False)

    graph_result = validate(graph_config)
    assert graph_result.returncode == 0, graph_result.stdout + graph_result.stderr
    assert not (cp / "data/fr_content_lock.json").exists()

    content_config_path = checkpoint._config(project, "debat_test", work_id, cp, "content", None)
    content_config = json.loads(content_config_path.read_text(encoding="utf-8"))
    content_result = validate(content_config)
    assert content_result.returncode != 0
    report = json.loads(content_result.stdout)
    assert report["summary"]["errors"] > 0
