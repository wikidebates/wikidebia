from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from wikidebia_validator.coherence import validate_coherence
from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report
from wikidebia_validator.wikicode import _validate_interlanguage, parse_template
from wikidebia_validator.workflow import validate_workflow


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _context(tmp_path: Path, *, norm: str = "1.2.34", deferred: bool = True, node_count: int = 9) -> tuple[PackageContext, dict, dict]:
    debate_id = "deferred_demo"
    nodes = []
    pages = [{"page_id": debate_id, "page_type": "debate", "language": "fr", "canonical_title": "Débat français", "status": "validated"}]
    for index in range(1, node_count + 1):
        node_id = f"A{index:04d}"
        nodes.append({
            "id": node_id,
            "status": "active",
            "fr": {"canonical_title": f"Argument français {index}", "displayed_title": f"Argument {index}", "title_status": "locked", "rubriques": [], "keywords": []},
            "en": {"canonical_title": None, "displayed_title": None, "title_status": "unassigned", "sections": [], "keywords": []},
            "pages": {"fr": {"generation": {"status": "validated"}}, "en": {"generation": {"status": "pending"}}},
            "derived": {"primary_occurrence_id": f"O{index:04d}"},
        })
        pages.append({"page_id": node_id, "page_type": "argument", "language": "fr", "canonical_title": f"Argument français {index}", "status": "validated"})
    registry = {
        "schema": {"mediawiki_structure_version": "1.0", "render_profile_version": "1.0", "registry_version": "1.0", "graph_version": "1.0", "validator_version": "0.4.36"},
        "debate": {
            "id": debate_id,
            "pages": {
                "fr": {"canonical_title": "Débat français", "title_status": "locked"},
                "en": {"canonical_title": None, "title_status": "unassigned"},
            },
        },
        "graph": {"lifecycle": {"status": "locked"}, "nodes": nodes, "edges": [], "occurrences": []},
    }
    validations = [
        {"scope": scope, "result": "passed", "blocking_errors": 0}
        for scope in ("graph", "fr_debate", "fr_global")
    ]
    manifest = {
        "debate_id": debate_id,
        "global_status": "release_ready",
        "created_at": "2026-08-05T12:00:00+02:00",
        "updated_at": "2026-08-05T12:00:00+02:00",
        "normative_versions": {"consolidated_norm": norm, "mediawiki_structure": "1.0", "render_profile": "1.0", "registry": "1.0", "graph": "1.0", "validator": "0.4.36"},
        "translation_status": {"en": "deferred" if deferred else "ready"},
        "core_files": {"registry": "data/registre_debat.json", "scope": "scope.json", "graph_json": "graph/graphe_argumentatif.json", "sources": "data/sources.json"},
        "pages": pages,
        "validations": validations,
        "works": [],
        "release": {},
    }
    _write(tmp_path / "manifest.json", manifest)
    _write(tmp_path / "data/registre_debat.json", registry)
    _write(tmp_path / "scope.json", {"debate_id": debate_id})
    _write(tmp_path / "data/sources.json", {"debate_id": debate_id, "sources": []})
    _write(tmp_path / "graph/graphe_argumentatif.json", {"debate": {"title_fr": "Débat français", "labels": None}})
    report = Report("0.4.36", str(tmp_path), ["workflow"])
    return PackageContext(tmp_path, report), manifest, registry


def _codes(ctx: PackageContext) -> list[str]:
    return [finding.code for finding in ctx.report.findings]


def test_deferred_french_release_with_ten_pages_does_not_require_english_titles(tmp_path: Path) -> None:
    ctx, _, _ = _context(tmp_path, node_count=9)  # one debate + nine arguments
    validate_workflow(ctx)
    assert "WDV-WF-005" not in _codes(ctx)
    assert not any("Pages en manquantes" in finding.message for finding in ctx.report.findings)
    assert ctx.report.metrics["workflow"]["english_translation_deferred"] is True


def test_deferred_mode_still_rejects_locked_english_title_without_value(tmp_path: Path) -> None:
    ctx, _, registry = _context(tmp_path)
    registry["graph"]["nodes"][0]["en"]["title_status"] = "locked"
    _write(tmp_path / "data/registre_debat.json", registry)
    ctx.cache.clear()
    validate_workflow(ctx)
    assert "WDV-WF-005" in _codes(ctx)


def test_deferred_french_wikicode_accepts_absent_interlanguage_parameter(tmp_path: Path) -> None:
    ctx, _, registry = _context(tmp_path)
    tmpl = parse_template("{{Argument\n|résumé=Texte français.\n|rubriques=Philosophie\n}}\n")
    _validate_interlanguage(ctx, tmpl, "output/fr/A0001.wiki", "fr", "argument", "A0001", registry, False)
    assert "WDV-MWK-011" not in _codes(ctx)


def test_deferred_french_wikicode_rejects_link_without_locked_target(tmp_path: Path) -> None:
    ctx, _, registry = _context(tmp_path)
    tmpl = parse_template("{{Argument\n|résumé=Texte.\n|interlangue={{Lien interlangue\n|langue=en\n|page=Invented title\n}}\n}}\n")
    _validate_interlanguage(ctx, tmpl, "output/fr/A0001.wiki", "fr", "argument", "A0001", registry, False)
    assert "WDV-MWK-011" in _codes(ctx)


def test_deferred_mode_rejects_english_manifest_page_without_locked_title(tmp_path: Path) -> None:
    ctx, manifest, _ = _context(tmp_path)
    manifest["pages"].append({"page_id": "A0001", "page_type": "argument", "language": "en", "canonical_title": "Invented", "status": "validated"})
    _write(tmp_path / "manifest.json", manifest)
    ctx.cache.clear()
    validate_coherence(ctx)
    assert "WDV-WF-005" in _codes(ctx)


def test_norm_1233_without_explicit_deferred_status_remains_strict(tmp_path: Path) -> None:
    ctx, manifest, _ = _context(tmp_path, norm="1.2.33", deferred=False)
    manifest.pop("translation_status", None)
    _write(tmp_path / "manifest.json", manifest)
    ctx.cache.clear()
    validate_workflow(ctx)
    assert "WDV-WF-005" in _codes(ctx)


def test_later_ready_translation_accepts_locked_target_and_french_link(tmp_path: Path) -> None:
    ctx, manifest, registry = _context(tmp_path, deferred=False)
    manifest["global_status"] = "fr_validated"
    registry["graph"]["nodes"][0]["en"].update({"canonical_title": "English argument 1", "displayed_title": "English argument 1", "title_status": "locked"})
    _write(tmp_path / "manifest.json", manifest)
    _write(tmp_path / "data/registre_debat.json", registry)
    ctx.cache.clear()
    tmpl = parse_template("{{Argument\n|résumé=Texte.\n|interlangue={{Lien interlangue\n|langue=en\n|page=English argument 1\n}}\n}}\n")
    _validate_interlanguage(ctx, tmpl, "output/fr/A0001.wiki", "fr", "argument", "A0001", registry, False)
    assert "WDV-MWK-011" not in _codes(ctx)


def test_schema_declares_translation_status_and_deferred_interlanguage() -> None:
    schema_root = Path(__file__).parents[1] / "src" / "wikidebia_validator" / "schemas"
    package_schema = json.loads((schema_root / "debate_package.schema.json").read_text(encoding="utf-8"))
    common_schema = json.loads((schema_root / "common.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(package_schema)
    Draft202012Validator.check_schema(common_schema)
    assert "deferred" in package_schema["properties"]["translation_status"]["properties"]["en"]["enum"]
    assert "deferred" in common_schema["$defs"]["interlanguageStatusFr"]["enum"]
