from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import Any

from jsonschema import FormatChecker
from jsonschema.validators import validator_for
from referencing import Registry, Resource

from .package import PackageContext


SCHEMA_BY_PATH = {
    "manifest.json": "debate_package.schema.json",
    "scope.json": "scope.schema.json",
    "data/registre_debat.json": "argument_registry.schema.json",
    "data/sources.json": "source_registry.schema.json",
    "data/lots_fr.json": "batch_collection.schema.json",
    "data/lots_en.json": "batch_collection.schema.json",
    "graph/graphe_argumentatif.json": "argument_graph.schema.json",
    "patches/interlanguage_fr.json": "interlanguage_patch.schema.json",
    "patches/interlanguage_fr.validated.json": "interlanguage_patch.schema.json",
    "release_manifest.json": "release_manifest.schema.json",
    "normative/requirements_catalog_wikidebia.json": "requirements_catalog.schema.json",
    "data/remote_migrations.json": "remote_migrations.schema.json",
}


class SchemaStore:
    def __init__(self) -> None:
        schema_dir = files("wikidebia_validator").joinpath("schemas")
        self.schemas: dict[str, dict[str, Any]] = {}
        for item in schema_dir.iterdir():
            if item.name.endswith(".schema.json"):
                doc = json.loads(item.read_text(encoding="utf-8"))
                self.schemas[item.name] = doc
        pairs = [(name, Resource.from_contents(doc)) for name, doc in self.schemas.items()]
        self.registry = Registry().with_resources(pairs)
        self.format_checker = FormatChecker()

    def validate(self, instance: Any, schema_name: str) -> list[Any]:
        schema = self.schemas[schema_name]
        cls = validator_for(schema)
        cls.check_schema(schema)
        validator = cls(schema, registry=self.registry, format_checker=self.format_checker)
        return sorted(validator.iter_errors(instance), key=lambda e: (list(e.absolute_path), e.message))


def pointer(path: Any) -> str:
    parts = []
    for part in path:
        s = str(part).replace("~", "~0").replace("/", "~1")
        parts.append(s)
    return "/" + "/".join(parts) if parts else "/"


def validate_instance(ctx: PackageContext, store: SchemaStore, rel: str, schema_name: str, instance: Any | None = None) -> None:
    if instance is None:
        instance = ctx.load_json(rel)
    if instance is None:
        return
    try:
        errors = store.validate(instance, schema_name)
    except Exception as exc:
        ctx.report.error("WDV-SCH-002", f"Impossible d'appliquer {schema_name} : {exc}", path=rel)
        return
    for err in errors:
        ctx.report.error("WDV-SCH-003", err.message, path=rel, pointer=pointer(err.absolute_path), details={"schema": schema_name})


def validate_all_schemas(ctx: PackageContext, store: SchemaStore) -> None:
    manifest = ctx.manifest()
    core = ctx.core_paths()
    mapping = dict(SCHEMA_BY_PATH)
    mapping[core["scope"]] = "scope.schema.json"
    mapping[core["registry"]] = "argument_registry.schema.json"
    mapping[core["graph_json"]] = "argument_graph.schema.json"
    mapping[core["sources"]] = "source_registry.schema.json"
    for rel, schema in mapping.items():
        if ctx.exists(rel):
            validate_instance(ctx, store, rel, schema)
    controls = (manifest or {}).get("editorial_controls") or {}
    for path_key, schema_name in (
        ("keyword_vocabulary_path", "keyword_vocabulary.schema.json"),
        ("summary_style_review_path", "summary_style_review.schema.json"),
        ("manual_remote_adoption_path", "manual_remote_adoptions.schema.json"),
        ("argument_name_assignment_path", "argument_name_assignments.schema.json"),
        ("argument_name_discovery_path", "argument_name_discovery_review.schema.json"),
        ("documentary_resource_registry_path", "documentary_resource_registry.schema.json"),
        ("semantic_convergence_review_path", "semantic_convergence_review.schema.json"),
    ):
        rel = controls.get(path_key)
        if rel and ctx.exists(rel):
            validate_instance(ctx, store, rel, schema_name)
    preservation = controls.get("legacy_content_preservation") or {}
    if preservation.get("enabled") is True:
        rel = preservation.get("lock_path")
        if rel and ctx.exists(rel):
            validate_instance(ctx, store, rel, "historical_content_lock.schema.json")
    if manifest:
        for i, page in enumerate(manifest.get("pages", [])):
            validate_instance(ctx, store, "manifest.json", "page_manifest.schema.json", page)
        for batch in manifest.get("batches", []):
            validate_instance(ctx, store, "manifest.json", "batch_manifest.schema.json", batch)
    for path in sorted(ctx.iter_files("manifests/pages/**/*.json")):
        validate_instance(ctx, store, ctx.relative(path), "page_manifest.schema.json")
    for path in sorted(ctx.iter_files("manifests/batches/**/*.json")):
        validate_instance(ctx, store, ctx.relative(path), "batch_manifest.schema.json")
    for path in sorted(ctx.iter_files("handoff/*.json")):
        validate_instance(ctx, store, ctx.relative(path), "handoff.schema.json")
    for path in sorted(ctx.iter_files("**/*receipt*.json")):
        validate_instance(ctx, store, ctx.relative(path), "archive_receipt.schema.json")
    for path in sorted(ctx.iter_files("logs/*.jsonl")):
        rel = ctx.relative(path)
        for line_no, obj in ctx.load_jsonl(rel):
            before = len(ctx.report.findings)
            validate_instance(ctx, store, rel, "operation_log_entry.schema.json", obj)
            for finding in ctx.report.findings[before:]:
                if finding.pointer:
                    object.__setattr__(finding, "pointer", f"ligne {line_no}{finding.pointer}")
