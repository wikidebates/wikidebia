from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


review = load_module("wikidebia_editorial_review")


def _write_validator_package(base: Path, *, result: str, version: str) -> None:
    package = base / "wikidebia_validator"
    package.mkdir(parents=True, exist_ok=True)
    (package / "__init__.py").write_text("\n", encoding="utf-8")
    (package / "cli.py").write_text(
        """
import json, sys
from pathlib import Path
args=sys.argv[1:]
json_out=Path(args[args.index('--json-output')+1])
text_out=Path(args[args.index('--text-output')+1])
result=%r
version=%r
report={
  'schema':'wikidebia-validator-report-1.0',
  'schema_version':'1.0',
  'validator_version':version,
  'producer':{'component':'validator','version':version},
  'result':result,
  'summary':{'errors':0 if result=='passed' else 1,'warnings':0},
  'findings':[] if result=='passed' else [{'level':'ERROR','code':'HOSTILE','path':None,'pointer':None,'message':'wrong validator imported'}],
}
json_out.parent.mkdir(parents=True,exist_ok=True)
json_out.write_text(json.dumps(report),encoding='utf-8')
text_out.write_text(result+'\\n',encoding='utf-8')
sys.exit(0 if result=='passed' else 1)
""" % (result, version),
        encoding="utf-8",
    )


def test_run_validator_uses_exact_project_validator_even_when_cwd_contains_hostile_copy(tmp_path, monkeypatch):
    project = tmp_path / "project"
    package = project / "package"
    package.mkdir(parents=True)
    (project / "validator" / "src").mkdir(parents=True)
    # Correct validator under the installed component.
    _write_validator_package(project / "validator" / "src", result="passed", version=review.VALIDATOR_VERSION)
    # Hostile/stale top-level copy that would win through sys.path[0] if cwd were inherited.
    _write_validator_package(project, result="failed", version=review.VALIDATOR_VERSION)
    monkeypatch.chdir(project)
    monkeypatch.setenv("PYTHONPATH", str(project))

    json_output = package / "report.json"
    text_output = package / "report.txt"
    report = review._run_validator(
        project, package, scopes=("schema",), json_output=json_output, text_output=text_output
    )
    assert report["result"] == "passed"
    assert not (project / "outgoing").exists()
