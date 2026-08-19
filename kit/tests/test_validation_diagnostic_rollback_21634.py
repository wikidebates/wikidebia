from __future__ import annotations

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


wf = load_module("wikidebia_review_workflow")


def _diagnostic(path: Path, *, errors: int = 3) -> None:
    payload = {
        "schema": wf.DIAGNOSTIC_SCHEMA,
        "schema_version": "1.0",
        "debate_id": "vote_test",
        "error_count": errors,
    }
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("DIAGNOSTIC_PACKAGE.json", json.dumps(payload))
        z.writestr("ERRORS.json", json.dumps({"error_count": errors, "errors": []}))


def test_review_import_rollback_preserves_complete_validation_diagnostic(tmp_path):
    project = tmp_path / "project"
    outgoing = project / "outgoing"
    outgoing.mkdir(parents=True)
    # This simulates the transaction snapshot taken before mechanical advance.
    before = {"already-there.zip"}
    (outgoing / "already-there.zip").write_bytes(b"old")

    diagnostic = outgoing / "vote_test_render_preflight_diagnostic.zip"
    _diagnostic(diagnostic, errors=7)
    partial = outgoing / "partial-next-review.zip"
    partial.write_bytes(b"partial")

    wf._remove_new_children(
        outgoing,
        before,
        True,
        preserve=wf._is_persistent_validation_diagnostic,
    )

    assert diagnostic.is_file(), "the diagnostic must survive rollback"
    assert not partial.exists(), "ordinary partial outgoing artifacts must still be removed"
    assert (outgoing / "already-there.zip").is_file()


def test_rollback_does_not_preserve_fake_or_incomplete_diagnostic(tmp_path):
    outgoing = tmp_path / "outgoing"
    outgoing.mkdir()
    fake = outgoing / "vote_test_render_preflight_diagnostic.zip"
    with zipfile.ZipFile(fake, "w") as z:
        z.writestr("DIAGNOSTIC_PACKAGE.json", json.dumps({"schema": "wrong", "schema_version": "1.0", "error_count": 2}))

    wf._remove_new_children(outgoing, set(), True, preserve=wf._is_persistent_validation_diagnostic)
    assert not fake.exists()
