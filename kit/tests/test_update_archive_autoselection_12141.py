from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "wikidebia_manage.py"
spec = importlib.util.spec_from_file_location("wikidebia_manage_scope_1241", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_update_scope_is_fr_when_english_is_deferred(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "manifest.json").write_text(json.dumps({
        "translation_status": {"en": "deferred"},
        "pages": [{"language": "fr", "status": "validated", "file_path": "output/fr/debate.wiki"}],
    }), encoding="utf-8")
    assert module.resolve_update_scope(corpus, None) == "fr"


def test_update_scope_is_all_when_both_languages_are_publishable(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "manifest.json").write_text(json.dumps({
        "translation_status": {"en": "ready"},
        "pages": [
            {"language": "fr", "status": "validated", "file_path": "output/fr/debate.wiki"},
            {"language": "en", "status": "validated", "file_path": "output/en/debate.wiki"},
        ],
    }), encoding="utf-8")
    assert module.resolve_update_scope(corpus, None) == "all"


def test_explicit_update_scope_is_never_overridden(tmp_path: Path):
    assert module.resolve_update_scope(tmp_path, "en") == "en"
