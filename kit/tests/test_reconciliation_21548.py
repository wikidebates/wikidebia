from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def _run_isolated(test_file: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", f"tests/{test_file}"],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=30,
    )

def test_remote_update_module_passes_in_true_isolation():
    result = _run_isolated("test_wikidebia_remote_update.py")
    assert result.returncode == 0, result.stdout + result.stderr

def test_reference_note_module_passes_in_true_isolation():
    result = _run_isolated("test_reference_note_punctuation_1244.py")
    assert result.returncode == 0, result.stdout + result.stderr
