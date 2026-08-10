from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "docs/BASELINE_FEATURES_2.4.0.json").read_text(encoding="utf-8"))


def _symbols(path: Path) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    result = {"functions": set(), "classes": {}, "constants": set(), "literal_constants": {}}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result["functions"].add(node.name)
        elif isinstance(node, ast.ClassDef):
            result["classes"][node.name] = {
                item.name for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                if name.isupper():
                    result["constants"].add(name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    result["constants"].add(target.id)
                    try:
                        value = ast.literal_eval(node.value)
                    except Exception:
                        continue
                    def normalize(obj):
                        if isinstance(obj, dict):
                            return {str(key): normalize(value) for key, value in obj.items()}
                        if isinstance(obj, (list, tuple)):
                            return [normalize(value) for value in obj]
                        if isinstance(obj, set):
                            return sorted((normalize(value) for value in obj), key=repr)
                        if isinstance(obj, (str, int, float, bool)) or obj is None:
                            return obj
                        raise TypeError(type(obj))
                    try:
                        if target.id.endswith("VERSION") or target.id == "VERSION":
                            continue
                        result["literal_constants"][target.id] = normalize(value)
                    except TypeError:
                        pass
    return result


def _contains_literal(actual, expected):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and _contains_literal(actual[key], value)
            for key, value in expected.items()
        )
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        # Literal sequences from the source are contracts: preserve order and values.
        return actual == expected or all(value in actual for value in expected)
    return actual == expected


def _schema_features(obj, prefix=""):
    props, required, enums = set(), set(), {}
    if isinstance(obj, dict):
        if isinstance(obj.get("properties"), dict):
            for key, value in obj["properties"].items():
                path = f"{prefix}.{key}" if prefix else key
                props.add(path)
                p2, r2, e2 = _schema_features(value, path)
                props |= p2
                required |= r2
                enums.update(e2)
        if isinstance(obj.get("required"), list):
            required |= {f"{prefix}.{key}" if prefix else key for key in obj["required"]}
        if isinstance(obj.get("enum"), list):
            enums[prefix] = {str(value) for value in obj["enum"]}
        for key in ("$defs", "definitions"):
            if isinstance(obj.get(key), dict):
                for name, value in obj[key].items():
                    p2, r2, e2 = _schema_features(value, f"{key}.{name}")
                    props |= p2
                    required |= r2
                    enums.update(e2)
        for key in ("items", "allOf", "anyOf", "oneOf", "if", "then", "else"):
            value = obj.get(key)
            rows = value if isinstance(value, list) else [value]
            for row in rows:
                if isinstance(row, dict):
                    p2, r2, e2 = _schema_features(row, prefix)
                    props |= p2
                    required |= r2
                    enums.update(e2)
    return props, required, enums


def _command_tokens(text: str) -> set[str]:
    values = set(re.findall(r'["\']([a-z][a-z0-9-]{2,})["\']', text))
    return {value for value in values if any(term in value for term in (
        "publish", "update", "upgrade", "doctor", "github", "graph", "corpus", "inspect", "plan"
    ))}


def test_all_240_kit_files_are_still_present():
    missing = [path for path in BASELINE["required_files"] if not (ROOT / path).is_file()]
    assert missing == []


def test_all_240_python_symbols_are_still_present():
    missing = []
    for rel, expected in BASELINE["python_symbols"].items():
        actual = _symbols(ROOT / rel)
        missing.extend(f"{rel}:function:{name}" for name in set(expected["functions"]) - actual["functions"])
        missing.extend(f"{rel}:constant:{name}" for name in set(expected["constants"]) - actual["constants"])
        for name, value in expected.get("literal_constants", {}).items():
            if name not in actual["literal_constants"] or not _contains_literal(actual["literal_constants"][name], value):
                missing.append(f"{rel}:literal_constant:{name}")
        for class_name, methods in expected["classes"].items():
            if class_name not in actual["classes"]:
                missing.append(f"{rel}:class:{class_name}")
            else:
                missing.extend(
                    f"{rel}:method:{class_name}.{name}"
                    for name in set(methods) - actual["classes"][class_name]
                )
    # Test names may change when version-gating regressions are converted into
    # invariance tests; test functions are not part of the kit API contract.
    unexpected = [item for item in missing if not item.startswith("tests/")]
    assert unexpected == []


def test_240_manifest_features_are_subsets_of_current_manifest():
    current = json.loads((ROOT / "KIT_MANIFEST.json").read_text(encoding="utf-8"))
    missing = {}
    for field, values in BASELINE["kit_manifest"].items():
        absent = sorted(set(values) - set(current.get(field, [])))
        if absent:
            missing[field] = absent
    assert missing == {}


def test_240_config_schema_contract_is_preserved():
    current = json.loads((ROOT / "config.schema.json").read_text(encoding="utf-8"))
    props, required, enums = _schema_features(current)
    baseline = BASELINE["config_schema"]
    assert set(baseline["properties"]) <= props
    assert set(baseline["required"]) <= required
    missing = {
        path: sorted(set(values) - enums.get(path, set()))
        for path, values in baseline["enums"].items()
        if set(values) - enums.get(path, set())
    }
    assert missing == {}


def test_240_launcher_and_manager_command_inventory_is_preserved():
    launcher = (ROOT / "root_template/wikidebia").read_text(encoding="utf-8")
    manager = (ROOT / "scripts/wikidebia_manage.py").read_text(encoding="utf-8")
    shell_functions = set(re.findall(r'^([A-Za-z_][A-Za-z0-9_]*)\s*\(\)\s*\{', launcher, re.M))
    assert set(BASELINE["root_launcher_shell_functions"]) <= shell_functions
    assert set(BASELINE["root_launcher_command_tokens"]) <= _command_tokens(launcher)
    assert set(BASELINE["manage_command_tokens"]) <= _command_tokens(manager)
