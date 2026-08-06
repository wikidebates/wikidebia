from __future__ import annotations

import json
import re
from pathlib import Path

import jsonschema


def test_all_versioned_config_examples_match_active_schema_and_named_norm():
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "config.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    examples = sorted((root / "configs").glob("creation_*_*.example.json"))
    assert examples
    for path in examples:
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(data))
        assert not errors, f"{path.name}: {[e.message for e in errors]}"
        match = re.search(r"_(1\.2\.\d+)\.example\.json$", path.name)
        assert match, path.name
        requirements = data["manifest_requirements"]
        assert requirements["normative_versions.consolidated_norm"] == match.group(1)
        extra = set(requirements) - {"normative_versions.consolidated_norm"}
        if match.group(1) in {"1.2.34", "1.2.35", "1.2.36", "1.2.37", "1.2.38", "1.2.39", "1.2.40", "1.2.41", "1.2.42", "1.2.43", "1.2.44", "1.2.45", "1.2.46", "1.2.47"}:
            assert extra <= {"translation_status.en"}
        else:
            assert not extra
