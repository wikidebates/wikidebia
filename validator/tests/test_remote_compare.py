from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path


def load_module(root: Path):
    path = root / "scripts" / "wikidebia_remote_compare.py"
    spec = importlib.util.spec_from_file_location("wikidebia_remote_compare", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_remote_compare_is_read_only_and_fixture_mode(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    source = (root / "scripts" / "wikidebia_remote_compare.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_calls = {"save", "put", "editpage", "delete", "move", "submit"}
    called = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert called.isdisjoint(forbidden_calls)

    package = tmp_path / "package"
    fixture = tmp_path / "fixture"
    local = "{{Débat\n|sujet=Test\n|sujet-complet=le test\n|avancement=Débat construit\n}}\n"
    (package / "output/fr/debate").mkdir(parents=True)
    (package / "output/fr/debate/debate.wiki").write_text(local, encoding="utf-8")
    (fixture / "fr").mkdir(parents=True)
    (fixture / "fr/test.wiki").write_text(local, encoding="utf-8")
    manifest = {
        "pages": [{
            "page_id": "test", "language": "fr", "page_type": "debate",
            "canonical_title": "Test", "file_path": "output/fr/debate/debate.wiki",
        }]
    }
    (package / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    module = load_module(root)
    args = type("Args", (), {
        "package": str(package), "language": None, "page_type": None, "limit": None,
        "fixture_dir": str(fixture), "family": "wikidebia", "login": False,
    })()
    results, summary = module.compare(args)
    assert summary["publication_attempted"] is False
    assert summary["write_operations"] == 0
    assert summary["counts"] == {"identical": 1}
    assert results[0].exact_match is True
