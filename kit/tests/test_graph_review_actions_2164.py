from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
TESTS = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(TESTS))

import wikidebia_graph_actions as ga  # noqa: E402
import wikidebia_corpus_review as review  # noqa: E402
import wikidebia_corpus_build as common  # noqa: E402
from test_wikidebia_corpus_review import make_project  # noqa: E402


def _prepare_single_occurrence_merge(build: Path) -> tuple[str, str, str]:
    # Fixture has A0003 reused.  Merge A0001 into A0002 instead: both are roots,
    # unique and child-bearing, so first remove its child link to create a safe
    # leaf-like case for the action unit test.
    registry = json.loads((build / "data/registre_debat.json").read_text(encoding="utf-8"))
    graph = registry["graph"]
    # Remove A0001 -> A0003 from graph and source page for this local unit fixture.
    graph["edges"] = [e for e in graph["edges"] if e["parent_node_id"] != "A0001"]
    graph["occurrences"] = [o for o in graph["occurrences"] if not (o["node_id"] == "A0003" and o["parent_occurrence_id"] == "O00001")]
    # O00004 becomes primary occurrence for A0003.
    for o in graph["occurrences"]:
        if o["id"] == "O00004":
            o["occurrence_role"] = "primary"
    counts, per_node = ga.compute_derived(graph["nodes"], graph["edges"], graph["occurrences"])
    graph["derived_counts"] = counts
    for n in graph["nodes"]:
        n["derived"] = per_node[n["id"]]
    common.write_json(build / "data/registre_debat.json", registry)
    projection = json.loads((build / "graph/graphe_argumentatif.json").read_text(encoding="utf-8"))
    for key in ("nodes", "edges", "occurrences", "derived_counts"):
        projection[key] = graph[key]
    common.write_json(build / "graph/graphe_argumentatif.json", projection)
    a = build / "imports/fr/arguments/A0001.wiki"
    a.write_text(a.read_text(encoding="utf-8").replace("|justifications={{Justification|page=Argument C|titre-affiché=C soutient A}}", "|justifications="), encoding="utf-8")
    return "O00001", "A0001", "A0002"


def test_legacy_owner_phrase_becomes_merge_redirect() -> None:
    entry = {
        "occurrence_id": "O00050",
        "node_id": "A0050",
        "placement_status": "needs_merge",
        "rationale": "Suppression demandée explicitement par le propriétaire : retirer le nœud A0050, son unique occurrence O00050 et la relation E00038. A0033 est conservé comme argument substantiel.",
    }
    action = ga._legacy_action(entry)
    assert action == {
        "action": "merge_redirect",
        "occurrence_id": "O00050",
        "node_id": "A0050",
        "target_node_id": "A0033",
        "reason": entry["rationale"],
    }


def test_merge_redirect_removes_parent_link_and_requires_target_in_summary(tmp_path: Path) -> None:
    _project, build = make_project(tmp_path)
    oid, nid, target = _prepare_single_occurrence_merge(build)
    plan, desired, graph_result = ga.prepare_action_plan(build, "debat_test", [{
        "action": "merge_redirect", "occurrence_id": oid, "node_id": nid, "target_node_id": target,
    }])
    parent = next(x for x in plan["mutations"] if x["page_type"] == "debate")
    child = next(x for x in plan["mutations"] if x.get("page_id") == nid)
    assert "[[Argument B]]" in parent["edit_summary"]
    assert "Argument A" not in desired[parent["source_path"]]
    assert child["operation"] == "redirect"
    assert desired[child["source_path"]] == "#REDIRECTION [[Argument B]]\n"
    assert graph_result["removed_nodes"] == ["A0001"]


def test_relation_change_moves_model_between_parameters_without_touching_child_page(tmp_path: Path) -> None:
    _project, build = make_project(tmp_path)
    plan, desired, graph_result = ga.prepare_action_plan(build, "debat_test", [{
        "action": "relation_change", "occurrence_id": "O00003", "node_id": "A0003",
        "new_parent_occurrence_id": "O00001", "new_relation": "objection",
    }])
    touched = [x for x in plan["mutations"] if x["operation"] == "update"]
    assert len(touched) == 1
    text = desired[touched[0]["source_path"]]
    assert "|justifications=" in text
    assert "{{Objection|page=Argument C|titre-affiché=C soutient A}}" in text
    edge = next(e for e in graph_result["new_graph"]["edges"] if e["parent_node_id"] == "A0001" and e["child_node_id"] == "A0003")
    assert edge["relation"] == "objection"


class FakeRemote:
    def __init__(self, pages: dict[str, tuple[int, str]]) -> None:
        self.pages = dict(pages)
        self.deleted: list[tuple[str, str]] = []
        self.writes: list[tuple[str, str, str]] = []
        self.rev = 100
    def open_language(self, language, expected_user): pass
    def close_language(self): pass
    def assert_identity(self, expected_user): pass
    def user_rights(self): return {"edit", "delete"}
    def available_change_tags(self): return {"chatgpt"}
    def read_page(self, title):
        if title not in self.pages: return False, None, ""
        rev, text = self.pages[title]; return True, rev, text
    def write_page(self, *, title, text, summary, tags, expected_user, create_only, base_revision_id):
        assert not create_only and tags == ["chatgpt"]
        assert self.pages[title][0] == base_revision_id
        self.rev += 1; self.pages[title] = (self.rev, text); self.writes.append((title, text, summary)); return self.rev
    def read_revision(self, title, revision_id):
        rev, text = self.pages[title]
        if rev != revision_id: return None
        summary = next(s for t, _x, s in reversed(self.writes) if t == title)
        return {"revision_id": rev, "text": text, "summary": summary, "tags": ["chatgpt"]}
    def delete_page(self, *, title, reason, expected_user):
        self.deleted.append((title, reason)); self.pages.pop(title, None)


def test_remote_executor_preflights_then_uses_individual_summaries(tmp_path: Path, monkeypatch) -> None:
    project, build = make_project(tmp_path)
    oid, nid, target = _prepare_single_occurrence_merge(build)
    plan, desired, _ = ga.prepare_action_plan(build, "debat_test", [{
        "action": "merge_redirect", "occurrence_id": oid, "node_id": nid, "target_node_id": target,
    }])
    pages = {}
    for row in plan["mutations"]:
        source = (build / row["source_path"]).read_text(encoding="utf-8")
        pages[row["title"]] = (int(row["expected_revision_id"]), source)
    fake = FakeRemote(pages)
    monkeypatch.setattr(ga, "_adapter", lambda _root: (fake, "ChatGPT"))
    receipt = ga.execute_remote_plan(project, build, plan, desired)
    assert receipt["schema"] == ga.ACTION_RECEIPT_SCHEMA
    assert len(fake.writes) == 2  # parent + redirect
    assert all(summary != "Corrections" for _title, _text, summary in fake.writes)
    parent_summary = next(summary for title, _text, summary in fake.writes if title == "Débat test")
    assert "[[Argument B]]" in parent_summary


def test_prospective_validation_failure_prevents_any_remote_write(tmp_path: Path, monkeypatch) -> None:
    project, build = make_project(tmp_path)
    oid, nid, target = _prepare_single_occurrence_merge(build)
    review_path = build / "reviews/graph_placement_review.json"
    common.write_json(review_path, {"entries": [{
        "occurrence_id": oid, "node_id": nid,
        "correction": {"action": "merge_redirect", "target_node_id": target},
    }]})

    called = {"remote": False}
    def forbidden_remote(*args, **kwargs):
        called["remote"] = True
        raise AssertionError("remote execution must not start")
    monkeypatch.setattr(ga, "execute_remote_plan", forbidden_remote)

    try:
        ga.execute_review_actions(
            project, build, "debat_test",
            preflight_validator=lambda preview: {"status": "failed", "package": str(preview)},
        )
    except ga.GraphActionError as exc:
        assert "aucune écriture distante" in str(exc)
    else:
        raise AssertionError("a failed prospective validation must block")
    assert called["remote"] is False


def test_explicit_duplicate_parent_summary_must_link_destination(tmp_path: Path) -> None:
    _project, build = make_project(tmp_path)
    oid, nid, target = _prepare_single_occurrence_merge(build)
    try:
        ga.prepare_action_plan(build, "debat_test", [{
            "action": "merge_redirect", "occurrence_id": oid, "node_id": nid,
            "target_node_id": target, "edit_summary_parent": "Retrait d'un doublon",
        }])
    except ga.GraphActionError as exc:
        assert "[[Titre]]" in str(exc)
    else:
        raise AssertionError("duplicate summary without target wikilink must be rejected")

class LaggyRemote(FakeRemote):
    def __init__(self, pages):
        super().__init__(pages)
        self.read_revision_calls = 0
    def read_revision(self, title, revision_id):
        self.read_revision_calls += 1
        # Simulate MediaWiki replica/tag propagation after a successful edit:
        # first the revision is not visible, then metadata lacks the tag, then complete.
        if self.read_revision_calls == 1:
            return None
        observed = super().read_revision(title, revision_id)
        if self.read_revision_calls == 2 and observed is not None:
            observed = dict(observed)
            observed["tags"] = []
        return observed


def test_remote_executor_retries_exact_revision_after_replica_lag(tmp_path: Path, monkeypatch) -> None:
    project, build = make_project(tmp_path)
    oid, nid, target = _prepare_single_occurrence_merge(build)
    plan, desired, _ = ga.prepare_action_plan(build, "debat_test", [{
        "action": "merge_redirect", "occurrence_id": oid, "node_id": nid, "target_node_id": target,
    }])
    pages = {}
    for row in plan["mutations"]:
        source = (build / row["source_path"]).read_text(encoding="utf-8")
        pages[row["title"]] = (int(row["expected_revision_id"]), source)
    fake = LaggyRemote(pages)
    monkeypatch.setattr(ga, "_adapter", lambda _root: (fake, "ChatGPT"))
    monkeypatch.setattr(ga.time, "sleep", lambda _seconds: None)
    receipt = ga.execute_remote_plan(project, build, plan, desired)
    assert receipt["schema"] == ga.ACTION_RECEIPT_SCHEMA
    assert len(fake.writes) == 2
    assert fake.read_revision_calls >= 4


def test_remote_executor_resumes_verified_partial_write_without_rewriting(tmp_path: Path, monkeypatch) -> None:
    project, build = make_project(tmp_path)
    oid, nid, target = _prepare_single_occurrence_merge(build)
    plan, desired, _ = ga.prepare_action_plan(build, "debat_test", [{
        "action": "merge_redirect", "occurrence_id": oid, "node_id": nid, "target_node_id": target,
    }])
    pages = {}
    for row in plan["mutations"]:
        source = (build / row["source_path"]).read_text(encoding="utf-8")
        pages[row["title"]] = (int(row["expected_revision_id"]), source)
    fake = FakeRemote(pages)
    parent = next(row for row in plan["mutations"] if row["page_type"] == "debate")
    parent_desired = desired[parent["source_path"]]
    # Simulate the first write having succeeded before the prior process aborted.
    first_rev = fake.write_page(
        title=parent["title"], text=parent_desired, summary=parent["edit_summary"], tags=["chatgpt"],
        expected_user="ChatGPT", create_only=False, base_revision_id=int(parent["expected_revision_id"]),
    )
    assert first_rev > int(parent["expected_revision_id"])
    prior_writes = len(fake.writes)
    monkeypatch.setattr(ga, "_adapter", lambda _root: (fake, "ChatGPT"))
    receipt = ga.execute_remote_plan(project, build, plan, desired)
    parent_result = next(row for row in receipt["results"] if row["title"] == parent["title"])
    assert parent_result["status"] == "already_done"
    # Only the duplicate page redirect is newly written during the restart.
    assert len(fake.writes) == prior_writes + 1
