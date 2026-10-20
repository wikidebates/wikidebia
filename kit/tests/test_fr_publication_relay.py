from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

import wikidebia_fr_publication_relay as relay


def request_fixture(directory: Path, request_id="cannabis-fr-test"):
    directory.mkdir(parents=True)
    originals = {"Child": (10, "{{Argument|résumé=Source conservée}}\n"),
                 "Parent": (11, "{{Argument|justifications={{Justification|page=Child}}}}\n")}
    pages = []
    for title, (revision, before) in originals.items():
        after = before.replace("page=Child", "page=Renamed child")
        for folder, text in (("before", before), ("after", after)):
            (directory / folder).mkdir(exist_ok=True)
            (directory / folder / (title+".wiki")).write_text(text)
        pages.append({"page_id": title, "old_title": title,
                      "new_title": "Renamed child" if title == "Child" else title,
                      "source_revision_id": revision, "source_sha256": relay.digest(before.encode()),
                      "target_sha256": relay.digest(after.encode()),
                      "before_file": "before/"+title+".wiki", "after_file": "after/"+title+".wiki"})
    request = {"schema": relay.SCHEMA, "request_id": request_id, "language": "fr", "site": relay.SITE,
               "authorization": "explicit_user_request", "pages": pages}
    save_request(directory, request)
    return request, originals


def save_request(directory, request):
    request["request_sha256"] = relay.request_hash(request)
    (directory / "request.json").write_text(json.dumps(request, ensure_ascii=False)+"\n")


class FakeWiki:
    def __init__(self, pages):
        self.pages = dict(pages)
        self.writes = []
        self.revisions = {}
        self.rights = {"edit", "move"}
        self.tags = {"chatgpt"}
        self.user = "ChatGPT"
        self.fail_after_move = False
        self.opened = False

    def open_language(self, language, expected_user):
        assert language == "fr"
        self.opened = True

    def close_language(self):
        self.opened = False

    def assert_identity(self, expected_user):
        if self.user != expected_user:
            raise relay.Blocked("Identité incorrecte")

    def user_rights(self):
        return self.rights

    def available_change_tags(self):
        return self.tags

    def assert_main_namespace(self, title):
        if ":" in title:
            raise relay.Blocked("Namespace interdit")

    def read_page(self, title):
        if title not in self.pages:
            return False, None, ""
        revision, text = self.pages[title]
        return True, revision, text

    def move_page(self, *, old_title, new_title, reason, expected_user, leave_redirect):
        assert leave_redirect
        assert new_title not in self.pages
        self.assert_identity(expected_user)
        self.pages[new_title] = self.pages.pop(old_title)
        self.pages[old_title] = (100, "#REDIRECT [["+new_title+"]]\n")
        self.writes.append(("move", old_title, new_title))
        if self.fail_after_move:
            self.fail_after_move = False
            raise ConnectionError("Réponse perdue après renommage")

    def write_page(self, *, title, text, summary, tags, expected_user, create_only, base_revision_id):
        self.assert_identity(expected_user)
        assert not create_only and self.pages[title][0] == base_revision_id
        revision = 200 + len(self.writes)
        self.pages[title] = (revision, text)
        self.revisions[revision] = {"text": text, "user": self.user, "summary": summary, "tags": tags}
        self.writes.append(("update", title))
        return revision

    def read_revision(self, title, revision):
        return self.revisions[revision]


def publish(tmp_path, request_dir, wiki, *, execute=True):
    return relay.publish_request(tmp_path / "server", request_dir, wiki, "ChatGPT", execute=execute, delay=0)


def test_full_request_and_repeat_are_idempotent(tmp_path):
    directory = tmp_path / "request"
    _, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    receipt = publish(tmp_path, directory, wiki)
    assert receipt["status"] == "completed"
    assert wiki.pages["Renamed child"][1] == pages["Child"][1]
    assert "page=Renamed child" in wiki.pages["Parent"][1]
    assert relay.redirect_to(wiki.pages["Child"][1], "Renamed child")
    count = len(wiki.writes)
    assert publish(tmp_path, directory, wiki) == receipt
    assert len(wiki.writes) == count and not wiki.opened


def test_preflight_performs_no_mutations(tmp_path):
    directory = tmp_path / "request"
    _, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    assert publish(tmp_path, directory, wiki, execute=False)["status"] == "ready"
    assert not wiki.writes
    assert not (tmp_path / "server/.state/fr-publication-relay").exists()


@pytest.mark.parametrize("problem", ("stale_parent", "changed_parent", "collision", "rights", "identity", "tag"))
def test_all_pages_are_checked_before_any_write(tmp_path, problem):
    directory = tmp_path / "request"
    _, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    if problem == "stale_parent":
        wiki.pages["Parent"] = (12, pages["Parent"][1])
    elif problem == "changed_parent":
        wiki.pages["Parent"] = (11, "{{Argument|résumé=Édition tierce}}\n")
    elif problem == "collision":
        wiki.pages["Renamed child"] = (15, pages["Child"][1])
    elif problem == "rights":
        wiki.rights = {"edit"}
    elif problem == "identity":
        wiki.user = "Other"
    else:
        wiki.tags = set()
    with pytest.raises(relay.Blocked):
        publish(tmp_path, directory, wiki)
    assert not wiki.writes and not wiki.opened


def test_interruption_after_move_resumes_without_duplicate_move(tmp_path):
    directory = tmp_path / "request"
    _, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    wiki.fail_after_move = True
    with pytest.raises(ConnectionError):
        publish(tmp_path, directory, wiki)
    receipt = publish(tmp_path, directory, wiki)
    assert receipt["status"] == "completed" and receipt["attempt"] == 2
    assert sum(event[0] == "move" for event in wiki.writes) == 1
    assert any(event["operation"] == "move_requested" for event in receipt["events"])


@pytest.mark.parametrize("problem", ("before", "after", "hash", "path", "authorization", "language", "revision", "namespace"))
def test_invalid_requests_are_rejected(tmp_path, problem):
    directory = tmp_path / "request"
    request, pages = request_fixture(directory)
    if problem in {"before", "after"}:
        (directory / problem / "Child.wiki").write_text("tampered")
    elif problem == "hash":
        request["request_sha256"] = "0"*64
        (directory / "request.json").write_text(json.dumps(request))
    else:
        if problem == "path":
            request["pages"][0]["before_file"] = "../outside"
        elif problem == "authorization":
            request["authorization"] = "automatic_merge"
        elif problem == "language":
            request["language"] = "en"
        elif problem == "revision":
            request["pages"][0]["source_revision_id"] = True
        else:
            request["pages"][0]["new_title"] = "User:Renamed child"
        save_request(directory, request)
    wiki = FakeWiki(pages)
    with pytest.raises(relay.Blocked):
        publish(tmp_path, directory, wiki)
    assert not wiki.writes


def test_completed_request_id_cannot_be_reused(tmp_path):
    directory = tmp_path / "request"
    request, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    publish(tmp_path, directory, wiki)
    request["note"] = "different request"
    save_request(directory, request)
    with pytest.raises(relay.Blocked, match="réécrite"):
        publish(tmp_path, directory, wiki)


def test_queue_transport_uses_git_without_modifying_application_checkout(tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "--quiet", str(remote)], check=True)
    repo = tmp_path / "repo"
    repo.mkdir()
    relay.git(repo, "init", "--quiet", "--initial-branch=main")
    relay.git(repo, "config", "user.name", "Test")
    relay.git(repo, "config", "user.email", "test@example.invalid")
    relay.git(repo, "remote", "add", "origin", str(remote))
    (repo / "file").write_text("application remains unchanged\n")
    relay.git(repo, "add", "file")
    relay.git(repo, "commit", "-m", "application")
    head = relay.git(repo, "rev-parse", "HEAD")
    directory = tmp_path / "request"
    request, _ = request_fixture(directory)
    assert relay.enqueue(repo, directory, request["request_sha256"]) == "queued"
    assert relay.enqueue(repo, directory, request["request_sha256"]) == "already_queued"
    second = tmp_path / "second"
    other, _ = request_fixture(second, "cannabis-fr-second")
    assert relay.enqueue(repo, second, other["request_sha256"]) == "queued"
    extracted = relay.fetch_requests(repo, tmp_path / "extracted")
    assert {p.name for p in extracted} == {request["request_id"], other["request_id"]}
    assert all(relay.load_request(path) for path in extracted)
    assert relay.git(repo, "rev-parse", "HEAD") == head
    assert relay.git(repo, "status", "--porcelain") == ""


def test_queue_submission_requires_the_exact_approved_hash(tmp_path):
    directory = tmp_path / "request"
    request_fixture(directory)
    with pytest.raises(relay.Blocked, match="empreinte exacte"):
        relay.enqueue(tmp_path, directory, "wrong")


def test_missing_source_is_not_treated_as_a_successful_rename(tmp_path):
    directory = tmp_path / "request"
    _, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    wiki.pages["Renamed child"] = wiki.pages.pop("Child")
    with pytest.raises(relay.Blocked, match="Collision"):
        publish(tmp_path, directory, wiki)
    assert not wiki.writes


def test_receipt_symlink_does_not_overwrite_an_existing_file(tmp_path):
    directory = tmp_path / "request"
    _, pages = request_fixture(directory)
    target = tmp_path / "preserve"
    target.write_text("existing data")
    journal = tmp_path / "server/.state/fr-publication-relay"
    journal.mkdir(parents=True)
    (journal / "cannabis-fr-test.json").symlink_to(target)
    wiki = FakeWiki(pages)
    with pytest.raises(relay.Blocked, match="symbolique"):
        publish(tmp_path, directory, wiki)
    assert target.read_text() == "existing data" and not wiki.writes


def test_concurrent_edit_after_move_is_preserved(tmp_path):
    directory = tmp_path / "request"
    _, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    original_move = wiki.move_page
    def move_and_edit(**kwargs):
        original_move(**kwargs)
        wiki.pages["Parent"] = (40, "{{Argument|résumé=Édition concurrente}}\n")
    wiki.move_page = move_and_edit
    with pytest.raises(relay.Blocked, match="modifiée"):
        publish(tmp_path, directory, wiki)
    assert wiki.pages["Parent"] == (40, "{{Argument|résumé=Édition concurrente}}\n")
    assert sum(event[0] == "update" for event in wiki.writes) == 0


def test_remote_readback_must_confirm_user_tag_and_content(tmp_path):
    directory = tmp_path / "request"
    _, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    original_read = wiki.read_revision
    wiki.read_revision = lambda title, revision: {**original_read(title, revision), "user": "Other"}
    with pytest.raises(relay.Blocked, match="Relecture"):
        publish(tmp_path, directory, wiki)
    state = json.loads((tmp_path / "server/.state/fr-publication-relay/cannabis-fr-test.json").read_text())
    assert state["status"] == "blocked"


def test_worker_does_not_retry_editorial_conflicts_without_explicit_request(tmp_path, monkeypatch):
    import contextlib
    directory = tmp_path / "cannabis-fr-test"
    _, pages = request_fixture(directory)
    wiki = FakeWiki(pages)
    wiki.pages["Parent"] = (12, pages["Parent"][1])
    root = tmp_path / "server"
    monkeypatch.setattr(relay, "git", lambda root, *args: "main" if args[0] == "symbolic-ref" else "")
    monkeypatch.setattr(relay, "deployment_lock", lambda root: contextlib.nullcontext())
    monkeypatch.setattr(relay, "fetch_requests", lambda root, destination: [directory])
    monkeypatch.setattr(relay, "build_adapter", lambda root: (wiki, "ChatGPT"))
    with pytest.raises(relay.Blocked):
        relay.work_once(root, execute=True)
    wiki.pages["Parent"] = pages["Parent"]
    assert relay.work_once(root, execute=True) == []
    assert not wiki.writes
    assert relay.work_once(root, execute=True, retry="cannabis-fr-test")[0]["status"] == "completed"


def test_request_branch_cannot_supply_symlinks(tmp_path, monkeypatch):
    monkeypatch.setattr(relay, "git", lambda root, *args: "0"*40)
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: subprocess.CompletedProcess([], 0))
    tree = b"120000 blob " + b"0"*40 + b"\trequests/cannabis-fr-test/before/link\0"
    monkeypatch.setattr(subprocess, "check_output", lambda *args, **kwargs: tree)
    with pytest.raises(relay.Blocked, match="fichiers de données"):
        relay.fetch_requests(tmp_path, tmp_path / "extracted")
    assert not (tmp_path / "extracted").exists()
