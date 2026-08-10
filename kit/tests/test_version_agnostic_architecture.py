from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location("wd_refactor_" + name.replace(".", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    inserted = str(SCRIPTS) not in sys.path
    if inserted:
        sys.path.insert(0, str(SCRIPTS))
    try:
        spec.loader.exec_module(module)
    finally:
        if inserted:
            sys.path.remove(str(SCRIPTS))
    return module


def test_current_versions_have_single_source_of_truth():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    info = _load("wikidebia_release_info.py")
    assert info.NORM_VERSION == versions["norm"]
    assert info.VALIDATOR_VERSION == versions["validator"]
    assert info.KIT_VERSION == versions["kit"]


def test_legacy_publication_plan_label_is_normalized_by_schema_not_producer_version():
    info = _load("wikidebia_release_info.py")
    legacy = {"plan_version": "wikidebia-publication-plan-2.15.53"}
    assert info.canonical_publication_plan_schema(legacy) == ("wikidebia-publication-plan-1.0", "1.0")
    assert info.publication_plan_is_compatible(legacy)


def test_recent_producer_cannot_make_unknown_schema_compatible():
    info = _load("wikidebia_release_info.py")
    plan = {"schema": "wikidebia-publication-plan-99.0", "schema_version": "99.0", "kit_version": "99.99.99"}
    assert not info.publication_plan_is_compatible(plan)


def test_parameter_aliases_canonicalize_without_changing_value():
    update = _load("wikidebia_update.py")
    assert update._canonical_parameter_name("fr", "debate", "sujet-complet") == "sujet-développé"
    assert update._canonical_parameter_name("en", "debate", "complete-topic") == "expanded-topic"
    assert update._canonical_parameter_name("fr", "argument", "débat-détaillé") == "débat-dédié"
    assert update._canonical_parameter_name("en", "argument", "detailed-debate") == "dedicated-debate"
    assert update._canonical_parameter_name("fr", "argument", "nom") == "nom-consacré"
    assert update._canonical_parameter_name("en", "argument", "name") == "established-name"


def test_active_scripts_do_not_define_release_versions_locally():
    offenders=[]
    for path in SCRIPTS.glob("*.py"):
        if path.name == "wikidebia_release_info.py":
            continue
        text=path.read_text(encoding="utf-8")
        for name in ("KIT_VERSION", "VALIDATOR_VERSION", "NORM_VERSION", "REQUIRED_VALIDATOR_VERSION"):
            if f'{name} = "' in text:
                offenders.append(f"{path.name}:{name}")
    assert offenders == []


def test_release_equality_is_reserved_for_upgrade_manager():
    import ast
    offenders = []
    names = {"KIT_VERSION", "VALIDATOR_VERSION", "NORM_VERSION", "REQUIRED_VALIDATOR_VERSION"}
    for path in SCRIPTS.glob("*.py"):
        if path.name in {"wikidebia_release_info.py", "wikidebia_manage.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare):
                continue
            seen = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
            if seen & names:
                offenders.append(f"{path.name}:{node.lineno}")
    assert offenders == []


def test_config_schema_does_not_pin_producer_release():
    schema = json.loads((ROOT / "config.schema.json").read_text(encoding="utf-8"))
    assert "const" not in schema["properties"]["kit_version"]
    assert "const" not in schema["properties"]["validator"]["properties"]["required_version"]
