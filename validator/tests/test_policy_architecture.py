from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "wikidebia_validator"


def _schema() -> dict:
    return json.loads((SRC / "schemas" / "debate_package.schema.json").read_text(encoding="utf-8"))


def test_consolidated_norm_is_trace_metadata_not_an_enumerated_feature_flag():
    schema = _schema()
    prop = json.loads((SRC / "schemas" / "common.schema.json").read_text(encoding="utf-8"))["$defs"]["normativeVersions"]["properties"]["consolidated_norm"]
    assert "$ref" in prop
    assert "enum" not in prop
    assert not schema.get("allOf")


def test_editorial_policy_revision_fields_are_not_schema_activation_switches():
    schema = _schema()
    schema_text = json.dumps(schema, ensure_ascii=False)
    assert "policy_revision" in schema_text or "_revision" in schema_text

    forbidden = {"consolidated_norm", "policy_revision", "argument_name_discovery_revision", "argument_name_assignment_revision", "manual_remote_adoption_revision"}
    bad: list[str] = []
    def walk(value, path="$"):
        if isinstance(value, dict):
            if "if" in value:
                condition_text = json.dumps(value["if"], ensure_ascii=False)
                if any(token in condition_text for token in forbidden):
                    bad.append(path)
            for key, child in value.items():
                walk(child, f"{path}.{key}")
        elif isinstance(value, list):
            for i, child in enumerate(value):
                walk(child, f"{path}[{i}]")
    walk(schema)
    assert bad == []


def test_current_editorial_modules_do_not_branch_on_declared_norm_versions():
    modules = [
        "bilingual.py",
        "batches.py",
        "coherence.py",
        "graph.py",
        "schema_validation.py",
        "sources.py",
        "validator.py",
        "wikicode.py",
        "workflow.py",
        "translation.py",
    ]
    forbidden_names = {
        "consolidated_norm",
        "normative_revision",
        "quality_policy_revision",
        "summary_policy_revision",
        "argument_name_assignment_revision",
        "argument_name_discovery_revision",
        "manual_remote_adoption_revision",
    }
    comparison_nodes = (ast.Compare,)
    failures: list[str] = []
    for module in modules:
        tree = ast.parse((SRC / module).read_text(encoding="utf-8"), filename=module)
        for node in ast.walk(tree):
            if not isinstance(node, comparison_nodes):
                continue
            names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
            attrs = {n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)}
            suspicious = (names | attrs) & forbidden_names
            if suspicious:
                failures.append(f"{module}:{node.lineno}:{','.join(sorted(suspicious))}")
    assert failures == []


def test_self_audit_does_not_gate_active_checks_by_norm_revision():
    text = (ROOT / "scripts" / "self_audit.py").read_text(encoding="utf-8")
    assert 'implemented == "1.2.' not in text
    assert "implemented in {" not in text
    assert "implemented not in {" not in text


def test_active_normative_documents_do_not_reintroduce_version_gated_editorial_wording():
    normative_root = ROOT / "normative_reference"
    forbidden_phrases = (
        "pour les paquets 1.2.",
        "pour les corpus 1.2.",
        "paquets 1.2.x",
        "sous la norme 1.2.",
        "sous les normes 1.2.",
        "sous la politique 1.2.",
        "sous la révision 1.2.",
        "paquet déclarant la norme 1.2.",
        "for packages declaring norm 1.2.",
        "for norm 1.2.",
        "applicable à partir de 1.2.",
        "aux paquets qui les déclarent",
        "rendue sous 1.2.31",
        "conservent leur comportement historique jusqu’à migration explicite",
    )
    failures: list[str] = []
    for path in normative_root.rglob("*.md"):
        if "history" in path.parts or path.name == "CHANGELOG_NORMATIF.md":
            continue
        text = path.read_text(encoding="utf-8").casefold()
        for phrase in forbidden_phrases:
            if phrase.casefold() in text:
                failures.append(f"{path.relative_to(normative_root)}:{phrase}")

    catalog = json.loads((normative_root / "01_normes" / "requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    def inspect_catalog(value):
        if isinstance(value, dict):
            statement = value.get("statement")
            if value.get("disposition") == "active" and isinstance(statement, str):
                folded = statement.casefold()
                for phrase in forbidden_phrases:
                    if phrase.casefold() in folded:
                        failures.append(f"requirements_catalog:{value.get('id')}:{phrase}")
            for child in value.values():
                inspect_catalog(child)
        elif isinstance(value, list):
            for child in value:
                inspect_catalog(child)
    inspect_catalog(catalog)
    assert failures == []


def test_active_normative_changelog_has_no_duplicate_release_headings():
    import re
    changelog = ROOT / "normative_reference" / "01_normes" / "CHANGELOG_NORMATIF.md"
    versions = []
    for line in changelog.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,3}\s+(1\.\d+(?:\.\d+)?)\b", line)
        if match:
            versions.append(match.group(1))
    assert len(versions) == len(set(versions))
    numeric = [tuple(int(part) for part in version.split(".")) for version in versions]
    assert numeric == sorted(numeric, reverse=True)
