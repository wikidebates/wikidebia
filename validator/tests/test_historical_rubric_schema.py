from __future__ import annotations

import hashlib

import pytest

from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report
from wikidebia_validator.schema_validation import SchemaStore, validate_instance
from .helpers import dump, graph_projection, make_registry


SCHEMAS = ("argument_registry.schema.json", "argument_graph.schema.json")
RUBRICS = ["Droit", "Économie", "Politique", "Santé", "Société"]
SECTIONS = ["Law", "Economy", "Politics", "Health", "Society"]


def context_and_instance(tmp_path, schema, language="fr", *, origin=None, imported=False):
    registry = make_registry()
    node = registry["graph"]["nodes"][0]
    node[language]["rubriques" if language == "fr" else "sections"] = list(
        RUBRICS if language == "fr" else SECTIONS
    )
    if language == "en":
        node["en"].update({"canonical_title": "The measure would benefit society",
                           "displayed_title": "The measure would benefit society", "title_status": "draft"})
    pages = []
    if origin is not None:
        pages.append({"page_id": "A0001", "page_type": "argument", "language": language, **origin})
    dump(tmp_path / "manifest.json", {"pages": pages})
    if imported:
        path = "imports/fr/arguments/A0001.wiki"
        content = b"{{Argument|rubriques=Droit, Economie}}\n"
        (tmp_path / path).parent.mkdir(parents=True)
        (tmp_path / path).write_bytes(content)
        dump(tmp_path / "data/import_provenance.json", {
            "schema": "wikidebia-import-provenance-1.0",
            "pages": [{"kind": "argument", "page_id": "A0001", "revision_id": 42,
                       "import_path": path, "sha256": hashlib.sha256(content).hexdigest()}],
        })
    ctx = PackageContext(tmp_path, Report("test", "test", ["schema"]))
    instance = registry if schema == SCHEMAS[0] else graph_projection(registry)
    return ctx, instance


def findings(ctx, instance, schema):
    validate_instance(ctx, SchemaStore(), "fixture.json", schema, instance)
    return ctx.report.findings


@pytest.mark.parametrize("schema", SCHEMAS)
def test_historical_french_rubrics_are_not_limited_to_four(tmp_path, schema):
    ctx, instance = context_and_instance(tmp_path, schema, origin={"page_origin": "preexisting"})
    assert not findings(ctx, instance, schema)


@pytest.mark.parametrize("schema", SCHEMAS)
@pytest.mark.parametrize("language", ("fr", "en"))
def test_verified_import_allows_historical_classification_before_page_manifests(tmp_path, schema, language):
    ctx, instance = context_and_instance(tmp_path, schema, language, imported=True)
    assert not findings(ctx, instance, schema)


@pytest.mark.parametrize("schema", SCHEMAS)
def test_new_english_translation_keeps_historical_source_classification(tmp_path, schema):
    ctx, instance = context_and_instance(tmp_path, schema, "en", origin={
        "page_origin": "new", "source_page_origin": "preexisting",
    })
    assert not findings(ctx, instance, schema)


@pytest.mark.parametrize("schema", SCHEMAS)
@pytest.mark.parametrize("origin", (None, {"page_origin": "new"}))
@pytest.mark.parametrize("language", ("fr", "en"))
def test_unproven_or_new_classification_still_rejects_five_rubrics(tmp_path, schema, origin, language):
    ctx, instance = context_and_instance(tmp_path, schema, language, origin=origin)
    assert any(f.code == "WDV-SCH-003" and "too long" in f.message for f in findings(ctx, instance, schema))


@pytest.mark.parametrize("schema", SCHEMAS)
def test_modified_import_is_not_historical_evidence(tmp_path, schema):
    ctx, instance = context_and_instance(tmp_path, schema, imported=True)
    (tmp_path / "imports/fr/arguments/A0001.wiki").write_text("modified\n")
    assert any("too long" in f.message for f in findings(ctx, instance, schema))


@pytest.mark.parametrize("schema", SCHEMAS)
def test_explicit_new_french_page_does_not_inherit_import_exception(tmp_path, schema):
    ctx, instance = context_and_instance(tmp_path, schema, origin={"page_origin": "new"}, imported=True)
    assert any("too long" in f.message for f in findings(ctx, instance, schema))


@pytest.mark.parametrize("schema", SCHEMAS)
def test_historical_exception_preserves_enum_and_uniqueness_checks(tmp_path, schema):
    ctx, instance = context_and_instance(tmp_path, schema, origin={"page_origin": "preexisting"})
    node = instance["graph"]["nodes"][0] if schema == SCHEMAS[0] else instance["nodes"][0]
    node["fr"]["rubriques"] += ["Unknown", "Droit"]
    errors = findings(ctx, instance, schema)
    assert any("Unknown" in f.message for f in errors)
    assert any("non-unique" in f.message for f in errors)
    assert not any("too long" in f.message for f in errors)
