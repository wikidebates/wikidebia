from __future__ import annotations

import hashlib
import json
from types import SimpleNamespace

from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report
from wikidebia_validator.schema_validation import (
    _preserved_empty_rubrics,
    _preserved_keyword_duplicates,
)


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fixture(root):
    source = "{{Argument|date-création=2021-03-18}}\n"
    source_path = root / "imports/fr/arguments/A0001.wiki"
    source_path.parent.mkdir(parents=True)
    source_path.write_text(source, encoding="utf-8")
    page = {
        "kind": "argument",
        "page_id": "A0001",
        "import_path": "imports/fr/arguments/A0001.wiki",
        "revision_id": 42,
        "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
    }
    dump(root / "data/import_provenance.json", {
        "schema": "wikidebia-import-provenance-1.0",
        "pages": [page],
    })
    review = {
        "review_scope": "graph_and_titles",
        "status": "approved",
    }
    review_sha = hashlib.sha256(
        json.dumps(review, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    review["review_sha256"] = review_sha
    dump(root / "reviews/fr/page_metadata_review.json", review)
    dump(root / "data/fr_page_metadata_lock.json", {
        "schema": "wikidebia-fr-page-metadata-lock-1.0",
        "review_sha256": review_sha,
        "arguments": [{
            "entity_id": "A0001",
            "page_origin": "preexisting",
            "rubriques": [],
            "keywords": [],
            "decisions": {
                "rubriques": "deferred_to_content_review",
                "keywords": "deferred_to_content_review",
            },
            "attestations": {"classification_review_deferred": True},
        }],
    })
    dump(root / "manifest.json", {"pages": []})
    registry = {"graph": {"nodes": [{
        "id": "A0001",
        "fr": {"rubriques": [], "keywords": []},
    }]}}
    return PackageContext(root, Report("test", str(root), ["schema"])), registry


def error(field):
    return SimpleNamespace(
        validator="minItems",
        absolute_path=["graph", "nodes", 0, "fr", field],
    )


def test_title_checkpoint_accepts_only_proven_historical_empty_fields(tmp_path):
    ctx, registry = fixture(tmp_path)
    assert _preserved_empty_rubrics(
        ctx, "argument_registry.schema.json", registry, error("rubriques")
    )
    assert _preserved_keyword_duplicates(
        ctx, "argument_registry.schema.json", registry, error("keywords")
    )


def test_title_checkpoint_rejects_changed_import_or_unscoped_lock(tmp_path):
    ctx, registry = fixture(tmp_path)
    (tmp_path / "imports/fr/arguments/A0001.wiki").write_text(
        "{{Argument|mots-clés=sexisme}}\n", encoding="utf-8"
    )
    assert not _preserved_keyword_duplicates(
        ctx, "argument_registry.schema.json", registry, error("keywords")
    )
    lock = json.loads((tmp_path / "data/fr_page_metadata_lock.json").read_text(encoding="utf-8"))
    lock["arguments"][0]["attestations"]["classification_review_deferred"] = False
    dump(tmp_path / "data/fr_page_metadata_lock.json", lock)
    assert not _preserved_empty_rubrics(
        ctx, "argument_registry.schema.json", registry, error("rubriques")
    )


def test_title_checkpoint_rejects_a_tampered_signed_review(tmp_path):
    ctx, registry = fixture(tmp_path)
    review_path = tmp_path / "reviews/fr/page_metadata_review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["review_scope"] = "graph_and_titles_tampered"
    dump(review_path, review)
    assert not _preserved_keyword_duplicates(
        ctx, "argument_registry.schema.json", registry, error("keywords")
    )
