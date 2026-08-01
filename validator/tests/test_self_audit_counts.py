from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


def _build_minimal_package(tmp_path: Path, declared_count: int = 4, declared_test_count: int = 3, receipt_test_count: int | None = None) -> Path:
    root = tmp_path / "package"
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    source = Path(__file__).resolve().parents[1] / "scripts" / "self_audit.py"
    shutil.copy2(source, scripts / "self_audit.py")
    (root / "README.md").write_text("test\n", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs/TEST_REPORT.txt").write_text(
        f"Tests pytest : {declared_test_count} réussis, 0 échec\n",
        encoding="utf-8",
    )

    (root / "VERSIONS.json").write_text(json.dumps({"norm": "1", "validator": "1", "kit": "1"}, indent=2) + "\n", encoding="utf-8")

    files = []
    for rel in ("README.md", "VERSIONS.json", "docs/TEST_REPORT.txt", "scripts/self_audit.py"):
        raw = (root / rel).read_bytes()
        files.append({"path": rel, "size_bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    manifest = {
        "artifact": "test",
        "version": "1",
        "self_excluded": ["PACKAGE_MANIFEST_SHA256.json", "PACKAGE_RECEIPT.json"],
        "declared_file_count": 4,
        "declared_test_count": declared_test_count,
        "files": files,
    }
    manifest_path = root / "PACKAGE_MANIFEST_SHA256.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "package_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "declared_file_count": declared_count,
        "declared_test_count": declared_test_count if receipt_test_count is None else receipt_test_count,
    }
    (root / "PACKAGE_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return root


def test_self_audit_accepts_matching_declared_file_count(tmp_path):
    root = _build_minimal_package(tmp_path)
    result = subprocess.run([sys.executable, str(root / "scripts/self_audit.py")], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_self_audit_rejects_wrong_receipt_declared_file_count(tmp_path):
    root = _build_minimal_package(tmp_path / "files", declared_count=5)
    result = subprocess.run([sys.executable, str(root / "scripts/self_audit.py")], capture_output=True, text=True)
    assert result.returncode == 1
    assert "nombre de fichiers déclaré divergent dans le reçu" in result.stdout

    root = _build_minimal_package(tmp_path / "tests", receipt_test_count=4)
    result = subprocess.run([sys.executable, str(root / "scripts/self_audit.py")], capture_output=True, text=True)
    assert result.returncode == 1
    assert "nombre de tests déclaré divergent dans le reçu" in result.stdout


def test_self_audit_ignores_runtime_cache_files(tmp_path):
    root = _build_minimal_package(tmp_path)
    cache = root / ".pytest_cache"
    cache.mkdir()
    (cache / "CACHEDIR.TAG").write_text("cache\n", encoding="utf-8")
    pycache = root / "tests" / "__pycache__"
    pycache.mkdir(parents=True)
    (pycache / "generated.pyc").write_bytes(b"temporary")
    result = subprocess.run([sys.executable, str(root / "scripts/self_audit.py")], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_self_audit_rejects_duplicate_requirement_ids(tmp_path):
    root = _build_minimal_package(tmp_path)
    catalog = root / "normative_reference" / "01_normes" / "requirements_catalog_wikidebia.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_text(
        json.dumps({
            "requirements": [
                {"id": "DUP-001", "sources": [], "normative_files": []},
                {"id": "DUP-001", "sources": [], "normative_files": []},
            ],
            "source_aliases": {},
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    result = subprocess.run([sys.executable, str(root / "scripts/self_audit.py")], capture_output=True, text=True)
    assert result.returncode == 1
    assert "identifiant d'exigence dupliqué: DUP-001" in result.stdout
