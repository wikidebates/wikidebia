from pathlib import Path
import importlib.util, json, sys

SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"

def load(name):
    spec=importlib.util.spec_from_file_location(name,SCRIPTS/f"{name}.py")
    mod=importlib.util.module_from_spec(spec); assert spec and spec.loader
    sys.modules[spec.name]=mod; spec.loader.exec_module(mod); return mod

def _schema_props(schema):
    def find(o):
        if isinstance(o,dict):
            if "translation_semantic_review_schema_version" in o and "semantic_marker_engine_version" in o: return o
            for v in o.values():
                r=find(v)
                if r:return r
        elif isinstance(o,list):
            for v in o:
                r=find(v)
                if r:return r
    return find(schema)

def test_current_kit_emitted_schema_versions_are_accepted_by_current_sibling_validator():
    sibling=Path(__file__).resolve().parents[2]/"validator"/"src"/"wikidebia_validator"/"schemas"/"debate_package.schema.json"
    assert sibling.is_file(), f"validator sibling missing: {sibling}"
    schema=json.loads(sibling.read_text(encoding="utf-8")); props=_schema_props(schema)
    assert "1.4" in props["translation_semantic_review_schema_version"]["enum"]
    assert "1.3" in props["semantic_marker_engine_version"]["enum"]

def test_render_test_is_independent_of_collection_order():
    text=(Path(__file__).resolve().parent/"test_wikidebia_render.py").read_text(encoding="utf-8")
    assert "translation._run_validator = fake_validator" in text
