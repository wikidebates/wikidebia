from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "wikidebia_manage.py"
spec = importlib.util.spec_from_file_location("wikidebia_manage", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def _write_component_zip(path: Path, artifact: str, *, include_receipt: bool = False) -> None:
    versions = {"norm": "1.2.20", "validator": "0.4.25", "kit": "2.2.10"}
    payloads = {
        "VERSIONS.json": (json.dumps(versions, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        "README.md": f"# {artifact}\n".encode("utf-8"),
    }
    files = [
        {"path": name, "size_bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        for name, raw in sorted(payloads.items())
    ]
    version = {"wikidebia-normes": "1.2.20", "wikidebia-validator": "0.4.25", "wikidebia-kit": "2.2.10"}[artifact]
    manifest = {
        "artifact": artifact,
        "version": version,
        "normative_revision": "1.2.20",
        "declared_file_count": len(files),
        "declared_test_count": 0,
        "files": files,
    }
    manifest_raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with zipfile.ZipFile(path, "w") as bundle:
        for name, raw in payloads.items():
            bundle.writestr(name, raw)
        bundle.writestr("PACKAGE_MANIFEST_SHA256.json", manifest_raw)
        if include_receipt:
            receipt = {
                "receipt_version": "wikidebia-package-receipt-1.0",
                "artifact": artifact,
                "version": version,
                "normative_revision": "1.2.20",
                "package_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
                "declared_file_count": len(files),
                "declared_test_count": 0,
            }
            canonical = json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            receipt["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
            bundle.writestr("PACKAGE_RECEIPT.json", json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")


def test_component_inspector_accepts_and_verifies_optional_receipt(tmp_path: Path):
    archive = tmp_path / "wikidebia-kit.zip"
    _write_component_zip(archive, "wikidebia-kit", include_receipt=True)
    metadata = module.inspect_component_zip(archive)
    assert metadata["artifact"] == "wikidebia-kit"
    assert metadata["versions"]["kit"] == "2.2.10"


def test_single_complete_bundle_is_collected_from_updates(tmp_path: Path):
    updates = tmp_path / "updates"
    updates.mkdir()
    component_dir = tmp_path / "components"
    component_dir.mkdir()
    names = {
        "wikidebia-normes": "wikidebia-normes.zip",
        "wikidebia-validator": "wikidebia-validator.zip",
        "wikidebia-kit": "wikidebia-kit.zip",
    }
    for artifact, name in names.items():
        _write_component_zip(component_dir / name, artifact)
    outer = updates / "WIKIDEBIA_COMPLET.zip"
    with zipfile.ZipFile(outer, "w") as bundle:
        for name in names.values():
            bundle.write(component_dir / name, name)
        bundle.writestr("README.txt", "bundle complet")
    components, sources, workspace = module.collect_update_payload(tmp_path)
    assert set(components) == set(names)
    assert sources == [outer]
    assert workspace.is_dir()


def test_delivery_prefers_root_components_over_historical_corpus_inputs(tmp_path: Path):
    updates = tmp_path / "updates"
    updates.mkdir()
    active = tmp_path / "active"
    active.mkdir()
    historical = tmp_path / "historical"
    historical.mkdir()
    artifacts = ("wikidebia-normes", "wikidebia-validator", "wikidebia-kit")
    for artifact in artifacts:
        _write_component_zip(active / f"{artifact}.zip", artifact)
        _write_component_zip(historical / f"{artifact}.zip", artifact)
        # Make the historical copy bytewise divergent but still internally valid.
        with zipfile.ZipFile(historical / f"{artifact}.zip", "a") as bundle:
            bundle.comment = b"historical"
    corpus = tmp_path / "corpus.zip"
    with zipfile.ZipFile(corpus, "w") as bundle:
        for artifact in artifacts:
            bundle.write(historical / f"{artifact}.zip", f"technical_inputs/{artifact}.zip")
    delivery = updates / "WIKIDEBIA_LIVRAISON.zip"
    with zipfile.ZipFile(delivery, "w") as bundle:
        for artifact in artifacts:
            bundle.write(active / f"{artifact}.zip", f"{artifact}.zip")
        bundle.write(corpus, "debate-corpus.zip")
    components, sources, workspace = module.collect_update_payload(tmp_path)
    assert set(components) == set(artifacts)
    assert all(components[artifact].parent.name.startswith("wrapper-") for artifact in artifacts)
    assert sources == [delivery]
    assert workspace.is_dir()


def test_optional_receipt_with_bad_manifest_hash_is_rejected(tmp_path: Path):
    archive = tmp_path / "wikidebia-kit.zip"
    _write_component_zip(archive, "wikidebia-kit", include_receipt=True)
    rewritten = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive) as source, zipfile.ZipFile(rewritten, "w") as target:
        for info in source.infolist():
            raw = source.read(info.filename)
            if info.filename == "PACKAGE_RECEIPT.json":
                receipt = json.loads(raw.decode("utf-8"))
                receipt["package_manifest_sha256"] = "0" * 64
                body = dict(receipt); body.pop("receipt_sha256", None)
                receipt["receipt_sha256"] = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
                raw = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            target.writestr(info, raw)
    try:
        module.inspect_component_zip(rewritten)
    except module.ManagementError as exc:
        assert "Reçu incohérent" in str(exc)
    else:
        raise AssertionError("reçu incohérent accepté")


def test_scope_values_cover_requested_publication_modes():
    assert module.scope_values("all") == (["fr", "en"], [])
    assert module.scope_values("fr") == (["fr"], [])
    assert module.scope_values("en") == (["en"], [])
    assert module.scope_values("fr-debate") == (["fr"], ["debate"])
    assert module.scope_values("en-debate") == (["en"], ["debate"])


def test_generated_config_is_relative_and_debate_first(tmp_path: Path):
    (tmp_path / "config").mkdir()
    run_dir = tmp_path / "plans" / "demo" / "run"
    run_dir.mkdir(parents=True)
    path = module.publication_config(tmp_path, "demo", "all", run_dir)
    config = json.loads(path.read_text(encoding="utf-8"))
    assert config["project_root"] == "."
    assert config["pywikibot_dir"] == "private/pywikibot"
    assert config["corpus_root"] == "corpus/demo"
    assert config["operation"]["page_type_order"] == ["debate", "argument"]
    assert config["validator"]["required_version"] == "0.4.25"
    assert config["manifest_requirements"] == {}
    assert str(tmp_path) not in path.read_text(encoding="utf-8")


def test_gitignore_excludes_secrets_runtime_and_corpus():
    ignore = (SCRIPT.parents[1] / "root_template" / ".gitignore").read_text(encoding="utf-8")
    for token in (
        "/private/", "/corpus/", "/archives/", "/updates/", "/incoming/",
        "/logs/", "/plans/", "/configs/", "/apicache/", "/.gitconfig-wikidebia",
        "/user-config.py", "/user-password.cfg", "*.lwp", "throttle.ctrl",
    ):
        assert token in ignore


def test_portability_check_rejects_current_root_literal(tmp_path: Path):
    (tmp_path / "kit").mkdir()
    (tmp_path / "kit" / "bad.txt").write_text(str(tmp_path), encoding="utf-8")
    try:
        module.assert_portable_sources(tmp_path)
    except module.ManagementError as exc:
        assert "Chemin absolu" in str(exc)
    else:
        raise AssertionError("chemin absolu accepté")


def test_git_commit_sets_repository_identity_when_none_is_configured(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "empty-global-gitconfig"))
    (tmp_path / ".gitignore").write_text((SCRIPT.parents[1] / "root_template" / ".gitignore").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "tracked.txt").write_text("contenu\n", encoding="utf-8")
    module.git_commit_and_push(tmp_path, "Test", push=False)
    name = module.run(["git", "config", "--local", "--get", "user.name"], cwd=tmp_path, capture=True).stdout.strip()
    email = module.run(["git", "config", "--local", "--get", "user.email"], cwd=tmp_path, capture=True).stdout.strip()
    assert name == "Wikidéb’IA"
    assert email == "wikidebia@localhost"


def test_single_zip_in_incoming_is_selected_automatically(tmp_path: Path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    archive = incoming / "gpa_autorisation.zip"
    archive.write_bytes(b"not-opened-here")
    assert module.find_debate_archive(tmp_path, None) == archive


def test_multiple_zips_require_an_identifier(tmp_path: Path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    (incoming / "gpa_autorisation.zip").write_bytes(b"a")
    (incoming / "vote_obligatoire.zip").write_bytes(b"b")
    try:
        module.find_debate_archive(tmp_path, None)
    except module.ManagementError as exc:
        message = str(exc)
        assert "Plusieurs archives ZIP" in message
        assert "gpa_autorisation" in message
        assert "vote_obligatoire" in message
    else:
        raise AssertionError("plusieurs ZIP acceptés sans identifiant")


def test_identifier_selects_matching_zip_in_incoming(tmp_path: Path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    expected = incoming / "gpa_autorisation.zip"
    expected.write_bytes(b"a")
    (incoming / "vote_obligatoire.zip").write_bytes(b"b")
    assert module.find_debate_archive(tmp_path, "gpa_autorisation") == expected


def test_identifier_must_not_include_zip_extension(tmp_path: Path):
    (tmp_path / "incoming").mkdir()
    try:
        module.find_debate_archive(tmp_path, "gpa_autorisation.zip")
    except module.ManagementError as exc:
        assert "sans l’extension .zip" in str(exc)
    else:
        raise AssertionError("extension .zip acceptée dans l’identifiant")


def test_single_legacy_named_zip_uses_manifest_debate_id(tmp_path: Path):
    import zipfile

    incoming = tmp_path / "incoming"
    incoming.mkdir()
    archive = incoming / "education_sexualite_ecole_fr_en_release_ready_repaired_2026-07-31.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr("manifest.json", json.dumps({"debate_id": "education_sexualite_ecole"}))
        bundle.writestr("payload.txt", "contenu")

    assert module.find_debate_archive(tmp_path, None) == archive
    debate_id, target = module.install_debate_corpus(tmp_path, archive)
    assert debate_id == "education_sexualite_ecole"
    assert target == tmp_path / "corpus" / "education_sexualite_ecole"
    assert (target / "payload.txt").read_text(encoding="utf-8") == "contenu"


def test_explicit_archive_stem_may_differ_from_manifest_debate_id(tmp_path: Path):
    import zipfile

    incoming = tmp_path / "incoming"
    incoming.mkdir()
    selected = incoming / "ancienne_livraison_2026-07-31.zip"
    other = incoming / "autre_debat.zip"
    with zipfile.ZipFile(selected, "w") as bundle:
        bundle.writestr("manifest.json", json.dumps({"debate_id": "education_sexualite_ecole"}))
    other.write_bytes(b"non-selected")

    archive = module.find_debate_archive(tmp_path, "ancienne_livraison_2026-07-31")
    assert archive == selected
    debate_id, target = module.install_debate_corpus(tmp_path, archive)
    assert debate_id == "education_sexualite_ecole"
    assert target.name == "education_sexualite_ecole"


def test_legacy_incoming_debates_is_migrated_to_incoming(tmp_path: Path):
    legacy = tmp_path / "incoming" / "debates"
    legacy.mkdir(parents=True)
    archive = legacy / "gpa_autorisation.zip"
    archive.write_bytes(b"archive")
    backup = tmp_path / "archives" / "updates" / "test"
    backup.mkdir(parents=True)
    module.migrate_legacy_debate_inbox(tmp_path, backup)
    assert (tmp_path / "incoming" / "gpa_autorisation.zip").read_bytes() == b"archive"
    assert not legacy.exists()


def test_runtime_requirements_include_pywikibot_and_validator_dependencies():
    requirements = (SCRIPT.parents[1] / "root_template" / "requirements-runtime.txt").read_text(encoding="utf-8")
    for dependency in ("pywikibot", "jsonschema", "referencing", "pytest"):
        assert dependency in requirements


def test_launcher_bootstraps_virtual_environment_and_dependencies():
    launcher = (SCRIPT.parents[1] / "root_template" / "wikidebia").read_text(encoding="utf-8")
    assert '-m venv "$VENV"' in launcher
    assert '-m pip install' in launcher
    assert 'requirements-runtime.txt' in launcher
    assert 'pywikibot' in launcher
    assert 'runtime-requirements.sha256' in launcher


def test_runtime_report_detects_missing_environment(tmp_path: Path):
    (tmp_path / "requirements-runtime.txt").write_text("pywikibot\n", encoding="utf-8")
    report = module.runtime_environment_report(tmp_path)
    assert report["python_available"] is False
    assert "pywikibot" in report["missing_modules"]


def test_doctor_reports_missing_runtime_environment(tmp_path: Path):
    (tmp_path / "requirements-runtime.txt").write_text("pywikibot\n", encoding="utf-8")
    (tmp_path / "private" / "pywikibot").mkdir(parents=True)
    (tmp_path / "private" / "pywikibot" / "user-config.py").write_text("family='wikidebates'\n", encoding="utf-8")
    report = module.doctor(tmp_path)
    assert report["status"] == "failed"
    assert any(".venv/bin/python" in issue for issue in report["issues"])


def _init_git_repo(root: Path) -> None:
    module.run(["git", "init", "-b", "main"], cwd=root)
    module.run(["git", "config", "user.name", "Test"], cwd=root)
    module.run(["git", "config", "user.email", "test@example.invalid"], cwd=root)


def test_root_configs_is_ignored_but_kit_configs_is_trackable(tmp_path: Path):
    (tmp_path / ".gitignore").write_text((SCRIPT.parents[1] / "root_template" / ".gitignore").read_text(encoding="utf-8"), encoding="utf-8")
    _init_git_repo(tmp_path)
    ignored = module.run(["git", "check-ignore", "-q", "--no-index", "--", "configs/test.json"], cwd=tmp_path, check=False)
    allowed = module.run(["git", "check-ignore", "-q", "--no-index", "--", "kit/configs/example.json"], cwd=tmp_path, check=False)
    assert ignored.returncode == 0
    assert allowed.returncode != 0


def test_prepare_git_security_untracks_lwp_without_deleting_it(tmp_path: Path):
    (tmp_path / ".gitignore").write_text((SCRIPT.parents[1] / "root_template" / ".gitignore").read_text(encoding="utf-8"), encoding="utf-8")
    secret = tmp_path / "pywikibot-session.lwp"
    secret.write_text("cookie", encoding="utf-8")
    _init_git_repo(tmp_path)
    module.run(["git", "add", "-f", "pywikibot-session.lwp"], cwd=tmp_path)
    assert module.git_tracked_forbidden_paths(tmp_path) == ["pywikibot-session.lwp"]
    module.prepare_git_security(tmp_path)
    assert secret.is_file()
    assert module.git_tracked_forbidden_paths(tmp_path) == []


def test_git_security_detects_missing_required_ignore_rule(tmp_path: Path):
    (tmp_path / ".gitignore").write_text("/private/\n", encoding="utf-8")
    missing = module.gitignore_missing_rules(tmp_path)
    assert "*.lwp" in missing
    assert "/apicache/" in missing


def test_doctor_reports_tracked_sensitive_file(tmp_path: Path, monkeypatch):
    (tmp_path / ".gitignore").write_text((SCRIPT.parents[1] / "root_template" / ".gitignore").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "private" / "pywikibot").mkdir(parents=True)
    (tmp_path / "private" / "pywikibot" / "user-config.py").write_text("family='wikidebates'\n", encoding="utf-8")
    secret = tmp_path / "session.lwp"
    secret.write_text("cookie", encoding="utf-8")
    _init_git_repo(tmp_path)
    module.run(["git", "add", "-f", "session.lwp"], cwd=tmp_path)
    monkeypatch.setattr(module, "runtime_environment_report", lambda root: {"requirements_sha256":"x", "python_available":True, "missing_modules":[]})
    report = module.doctor(tmp_path)
    assert report["status"] == "failed"
    assert any("session.lwp" in issue for issue in report["issues"])


def test_runtime_requirements_bound_pywikibot_major_version():
    requirements = (SCRIPT.parents[1] / "root_template" / "requirements-runtime.txt").read_text(encoding="utf-8")
    assert "pywikibot>=11.5,<12" in requirements


def test_parser_exposes_github_sync_command():
    parser = module.build_parser()
    args = parser.parse_args(["github-sync"])
    assert args.command == "github-sync"


def test_git_push_disables_terminal_password_prompt(monkeypatch, tmp_path: Path):
    _init_git_repo(tmp_path)
    module.run(["git", "remote", "add", "origin", "https://github.com/example/example.git"], cwd=tmp_path)
    calls = []
    original = module.run
    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        if command[:2] == ["git", "push"]:
            import subprocess
            return subprocess.CompletedProcess(command, 1, stdout="", stderr="auth failed")
        return original(command, **kwargs)
    monkeypatch.setattr(module, "run", fake_run)
    assert module.git_push_current_branch(tmp_path, strict=False) is False
    push = next(item for item in calls if item[0][:2] == ["git", "push"])[1]
    assert push["env"]["GIT_TERMINAL_PROMPT"] == "0"


def test_forbidden_git_paths_keep_leading_dot_semantics():
    assert module.forbidden_git_path(".gitconfig-wikidebia")
    assert module.forbidden_git_path(".state/runtime.json")
    assert module.forbidden_git_path("kit/configs/example.json") is False


def test_github_sync_commits_pending_safe_changes_before_push(tmp_path: Path, monkeypatch):
    (tmp_path / ".gitignore").write_text((SCRIPT.parents[1] / "root_template" / ".gitignore").read_text(encoding="utf-8"), encoding="utf-8")
    _init_git_repo(tmp_path)
    (tmp_path / "safe.txt").write_text("contenu\n", encoding="utf-8")
    pushed = []
    monkeypatch.setattr(module, "git_push_current_branch", lambda root, strict: pushed.append((root, strict)) or True)
    module.github_sync(tmp_path)
    assert module.run(["git", "status", "--porcelain"], cwd=tmp_path, capture=True).stdout.strip() == ""
    assert module.run(["git", "log", "-1", "--pretty=%s"], cwd=tmp_path, capture=True).stdout.strip() == "Synchronisation sécurisée Wikidéb’IA"
    assert pushed == [(tmp_path, True)]


def test_publish_command_has_no_interactive_prompt(monkeypatch, tmp_path: Path):
    def forbidden_input(*args, **kwargs):
        raise AssertionError("input() ne doit jamais être appelé par publish")
    monkeypatch.setattr("builtins.input", forbidden_input)
    monkeypatch.setattr(module, "ensure_credentials", lambda root: None)
    archive = tmp_path / "incoming" / "demo.zip"
    archive.parent.mkdir(parents=True)
    archive.write_bytes(b"zip")
    monkeypatch.setattr(module, "find_debate_archive", lambda root, identifier: archive)
    corpus = tmp_path / "corpus" / "demo"
    corpus.mkdir(parents=True)
    monkeypatch.setattr(module, "install_debate_corpus", lambda root, selected: ("demo", corpus))
    monkeypatch.setattr(module, "publication_config", lambda root, debate_id, scope, run_dir: run_dir / "config.json")
    plan = {"blockers": [], "counts": {}, "actions": [], "plan_sha256": "a" * 64}
    def fake_run(command, *, cwd, capture=False, check=True, env=None):
        class Result:
            stdout = '{"created":0,"updated":0,"skipped":0}\n'
            returncode = 0
        if "--mode" in command and command[command.index("--mode") + 1] == "plan":
            output = Path(cwd) / command[command.index("--plan-output") + 1]
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(plan), encoding="utf-8")
        return Result()
    monkeypatch.setattr(module, "run", fake_run)
    result = module.publish_debate(tmp_path, None, "all", False, True)
    assert result == {"created": 0, "updated": 0, "skipped": 0}


def test_nested_complete_delivery_is_collected_from_one_zip(tmp_path: Path):
    updates=tmp_path/"updates"; updates.mkdir()
    component_dir=tmp_path/"components"; component_dir.mkdir()
    names=[]
    for artifact in module.COMPONENTS:
        name=artifact+".zip"; names.append(name)
        _write_component_zip(component_dir/name,artifact)
    inner=tmp_path/"WIKIDEBIA_SOURCES_COMPLETES.zip"
    with zipfile.ZipFile(inner,"w") as bundle:
        for name in names: bundle.write(component_dir/name,name)
    outer=updates/"WIKIDEBIA_LIVRAISON_COMPLETE.zip"
    with zipfile.ZipFile(outer,"w") as bundle:
        bundle.write(inner,"delivery/WIKIDEBIA_SOURCES_COMPLETES.zip")
        bundle.writestr("delivery/AUDIT.txt","ok")
    components,sources,workspace=module.collect_update_payload(tmp_path)
    assert set(components)==set(module.COMPONENTS)
    assert sources==[outer]
    assert workspace.is_dir()


def test_update_command_has_no_interactive_prompt(monkeypatch, tmp_path: Path):
    def forbidden_input(*args, **kwargs):
        raise AssertionError("input() ne doit jamais être appelé par update")
    monkeypatch.setattr("builtins.input", forbidden_input)
    monkeypatch.setattr(module, "ensure_credentials", lambda root: None)
    monkeypatch.setattr(module, "_prepare_update_corpus", lambda root, identifier: ("demo", None))
    monkeypatch.setattr(module, "remote_update_config", lambda root, debate_id, scope, run_dir: run_dir / "config.json")
    plan = {
        "counts": {"update": 1},
        "operations": {"blocked": []},
        "plan_sha256": "b" * 64,
    }
    calls = []
    def fake_run(command, *, cwd, capture=False, check=True, env=None):
        calls.append(command)
        class Result:
            stdout = '{"updated":1}\n'
            stderr = ""
            returncode = 0
        if "--mode" in command and command[command.index("--mode") + 1] == "plan":
            output = Path(cwd) / command[command.index("--plan-output") + 1]
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(plan), encoding="utf-8")
        return Result()
    monkeypatch.setattr(module, "run", fake_run)
    result = module.update_debate(tmp_path, "demo", "all", False, False, False, False, True)
    assert result["status"] == "executed"
    assert result["counts"] == {"updated": 1}
    execute = next(call for call in calls if "--mode" in call and call[call.index("--mode") + 1] == "execute")
    assert execute[execute.index("--confirm-plan-sha256") + 1] == "b" * 64


def test_update_yes_remains_a_hidden_compatibility_option():
    parser = module.build_parser()
    args = parser.parse_args(["update", "demo", "--yes"])
    assert args.command == "update"
    assert args.yes is True
    assert "--yes" not in parser.format_help()
