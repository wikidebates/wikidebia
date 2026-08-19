from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_physical_launcher_attests_loaded_core_modules(tmp_path):
    package = tmp_path / "package"
    package.mkdir()
    # A deliberately incomplete package is sufficient: we only require that a
    # report is emitted and carries the runtime attestation before any findings.
    (package / "manifest.json").write_text("{}\n", encoding="utf-8")
    out = tmp_path / "report.json"
    txt = tmp_path / "report.txt"
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            str(ROOT / "scripts" / "wikidebia_validate.py"),
            "validate",
            str(package),
            "--scope",
            "schema",
            "--format",
            "text",
            "--json-output",
            str(out),
            "--text-output",
            str(txt),
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert out.is_file(), completed.stderr
    report = json.loads(out.read_text(encoding="utf-8"))
    runtime = report["metrics"]["runtime_attestation"]
    assert runtime["mode"] == "component_script_isolated_v2"
    assert runtime["cli_sha256"] == hashlib.sha256(
        (ROOT / "src" / "wikidebia_validator" / "cli.py").read_bytes()
    ).hexdigest()
    assert runtime["editorial_sha256"] == hashlib.sha256(
        (ROOT / "src" / "wikidebia_validator" / "editorial.py").read_bytes()
    ).hexdigest()
    assert runtime["wikicode_sha256"] == hashlib.sha256(
        (ROOT / "src" / "wikidebia_validator" / "wikicode.py").read_bytes()
    ).hexdigest()
    assert runtime["historical_summary_sha256"] == hashlib.sha256(
        (ROOT / "src" / "wikidebia_validator" / "historical_summary.py").read_bytes()
    ).hexdigest()
