from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import zipfile
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


review = load_module("wikidebia_editorial_review")


def _project(tmp_path: Path) -> tuple[Path, Path]:
    project = tmp_path / "project"
    package = project / ".state" / "rendered-copy"
    validator_pkg = project / "validator" / "src" / "wikidebia_validator"
    validator_pkg.mkdir(parents=True)
    (validator_pkg / "cli.py").write_text("# cli\n", encoding="utf-8")
    (validator_pkg / "editorial.py").write_text("# editorial\n", encoding="utf-8")
    validator_scripts = project / "validator" / "scripts"
    validator_scripts.mkdir(parents=True)
    (validator_scripts / "wikidebia_validate.py").write_text("# launcher\n", encoding="utf-8")
    (project / "outgoing").mkdir(parents=True)
    (package / "reports").mkdir(parents=True)
    (package / "reviews").mkdir(parents=True)
    (package / "data").mkdir(parents=True)
    (package / "output" / "en" / "arguments").mkdir(parents=True)
    (package / "manifest.json").write_text(json.dumps({"debate_id": "vote_test", "work_id": "W1"}), encoding="utf-8")
    (package / "reviews" / "summary_style_review.json").write_text("{}\n", encoding="utf-8")
    (package / "data" / "en_content_lock.json").write_text("{}\n", encoding="utf-8")
    (package / "output" / "en" / "arguments" / "A0001.wiki").write_text("{{Argument}}\n", encoding="utf-8")
    return project, package


def _runtime(project: Path) -> dict[str, str]:
    pkg = project / "validator" / "src" / "wikidebia_validator"
    return {
        "mode": "component_script_isolated_v1",
        "cli_sha256": hashlib.sha256((pkg / "cli.py").read_bytes()).hexdigest(),
        "editorial_sha256": hashlib.sha256((pkg / "editorial.py").read_bytes()).hexdigest(),
    }


def test_failed_validator_exports_complete_diagnostic_zip(tmp_path, monkeypatch):
    project, package = _project(tmp_path)
    json_output = package / "reports" / "render_preflight.json"
    text_output = package / "reports" / "render_preflight.txt"
    findings = [
        {"level": "ERROR", "code": f"E{i:03d}", "path": "output/en/arguments/A0001.wiki", "pointer": None, "message": f"error {i}"}
        for i in range(1, 8)
    ]

    class Result:
        returncode = 1
        stderr = ""

    def fake_run(*args, **kwargs):
        report = {
            "schema": "wikidebia-validator-report-1.0",
            "schema_version": "1.0",
            "validator_version": review.VALIDATOR_VERSION,
            "result": "failed",
            "summary": {"errors": 7, "warnings": 0},
            "metrics": {"runtime_attestation": _runtime(project)},
            "findings": findings,
        }
        json_output.write_text(json.dumps(report), encoding="utf-8")
        text_output.write_text("validation failed\n", encoding="utf-8")
        return Result()

    monkeypatch.setattr(review.subprocess, "run", fake_run)
    try:
        review._run_validator(
            project,
            package,
            scopes=("schema", "editorial"),
            json_output=json_output,
            text_output=text_output,
        )
    except review.EditorialReviewError as exc:
        message = str(exc)
    else:
        raise AssertionError("validation failure expected")

    diagnostic = project / "outgoing" / "vote_test_render_preflight_diagnostic.zip"
    assert diagnostic.is_file()
    assert "diagnostic complet : outgoing/vote_test_render_preflight_diagnostic.zip" in message
    with zipfile.ZipFile(diagnostic) as bundle:
        names = set(bundle.namelist())
        assert {"DIAGNOSTIC_PACKAGE.json", "ERRORS.json", "ERRORS.txt", "README.txt"} <= names
        assert "context/reports/render_preflight.json" in names
        assert "context/reports/render_preflight.txt" in names
        assert "context/output/en/arguments/A0001.wiki" in names
        errors = json.loads(bundle.read("ERRORS.json"))
        assert errors["error_count"] == 7
        assert [row["code"] for row in errors["errors"]] == [f"E{i:03d}" for i in range(1, 8)]
        manifest = json.loads(bundle.read("DIAGNOSTIC_PACKAGE.json"))
        assert manifest["error_count"] == 7
        assert manifest["phase"] == "render_preflight"
        assert manifest["scopes"] == ["schema", "editorial"]


def test_diagnostic_export_failure_never_masks_validator_error(tmp_path, monkeypatch):
    project, package = _project(tmp_path)
    json_output = package / "reports" / "render_preflight.json"
    text_output = package / "reports" / "render_preflight.txt"

    class Result:
        returncode = 1
        stderr = ""

    def fake_run(*args, **kwargs):
        report = {
            "schema": "wikidebia-validator-report-1.0",
            "schema_version": "1.0",
            "validator_version": review.VALIDATOR_VERSION,
            "result": "failed",
            "summary": {"errors": 1, "warnings": 0},
            "metrics": {"runtime_attestation": _runtime(project)},
            "findings": [{"level": "ERROR", "code": "E001", "path": None, "pointer": None, "message": "boom"}],
        }
        json_output.write_text(json.dumps(report), encoding="utf-8")
        text_output.write_text("validation failed\n", encoding="utf-8")
        return Result()

    monkeypatch.setattr(review.subprocess, "run", fake_run)
    monkeypatch.setattr(review, "_create_validation_diagnostic_archive", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("disk")))
    try:
        review._run_validator(project, package, scopes=("schema",), json_output=json_output, text_output=text_output)
    except review.EditorialReviewError as exc:
        assert "E001" in str(exc)
    else:
        raise AssertionError("validator failure must remain blocking")
