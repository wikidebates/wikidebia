from __future__ import annotations

import hashlib
import importlib.util
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
    (package / "editorial.py").write_text("RUNTIME_MARKER='correct'\n", encoding="utf-8")
    cli = '''
import json, os
from pathlib import Path

def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('package')
    parser.add_argument('--scope', action='append', default=[])
    parser.add_argument('--format')
    parser.add_argument('--json-output')
    parser.add_argument('--text-output')
    args=parser.parse_args(argv)
    json_out=Path(args.json_output)
    text_out=Path(args.text_output)
    result=__RESULT__
    version=__VERSION__
    report={
      'schema':'wikidebia-validator-report-1.0',
      'schema_version':'1.0',
      'validator_version':version,
      'producer':{'component':'validator','version':version},
      'result':result,
      'metrics':{
        'runtime_attestation':{
          'mode':os.environ.get('WIKIDEBIA_VALIDATOR_RUNTIME_MODE',''),
          'cli_sha256':os.environ.get('WIKIDEBIA_VALIDATOR_RUNTIME_CLI_SHA256',''),
          'editorial_sha256':os.environ.get('WIKIDEBIA_VALIDATOR_RUNTIME_EDITORIAL_SHA256',''),
        }
      },
      'summary':{'errors':0 if result=='passed' else 1,'warnings':0},
      'findings':[] if result=='passed' else [{'level':'ERROR','code':'HOSTILE','path':None,'pointer':None,'message':'wrong validator imported'}],
    }
    json_out.parent.mkdir(parents=True,exist_ok=True)
    json_out.write_text(json.dumps(report),encoding='utf-8')
    text_out.write_text(result+'\\n',encoding='utf-8')
    return 0 if result=='passed' else 1
'''.replace('__RESULT__', repr(result)).replace('__VERSION__', repr(version))
    (package / "cli.py").write_text(cli, encoding="utf-8")


def _write_validator_launcher(project: Path) -> None:
    scripts = project / "validator" / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "wikidebia_validate.py").write_text(
        '''
from pathlib import Path
import hashlib, os, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=(ROOT/'src').resolve()
PACKAGE=(SRC/'wikidebia_validator').resolve()
sys.path.insert(0,str(SRC))
from wikidebia_validator import cli as _cli
from wikidebia_validator import editorial as _editorial
for module in (_cli,_editorial):
    Path(module.__file__).resolve().relative_to(PACKAGE)
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
os.environ['WIKIDEBIA_VALIDATOR_RUNTIME_MODE']='component_script_isolated_v1'
os.environ['WIKIDEBIA_VALIDATOR_RUNTIME_CLI_SHA256']=sha(_cli.__file__)
os.environ['WIKIDEBIA_VALIDATOR_RUNTIME_EDITORIAL_SHA256']=sha(_editorial.__file__)
raise SystemExit(_cli.main())
''',
        encoding="utf-8",
    )


def test_run_validator_uses_physical_isolated_launcher_even_with_hostile_paths(tmp_path, monkeypatch):
    project = tmp_path / "project"
    package = project / "package"
    package.mkdir(parents=True)
    (project / "validator" / "src").mkdir(parents=True)

    _write_validator_package(project / "validator" / "src", result="passed", version=review.VALIDATOR_VERSION)
    _write_validator_launcher(project)
    _write_validator_package(project, result="failed", version=review.VALIDATOR_VERSION)

    hostile = tmp_path / "hostile"
    _write_validator_package(hostile, result="failed", version=review.VALIDATOR_VERSION)
    (project / "validator" / "src" / "sitecustomize.py").write_text(
        f"import sys\nsys.path.insert(0, {str(hostile)!r})\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(project)
    monkeypatch.setenv("PYTHONPATH", str(project))

    json_output = package / "report.json"
    text_output = package / "report.txt"
    report = review._run_validator(
        project, package, scopes=("schema",), json_output=json_output, text_output=text_output
    )
    assert report["result"] == "passed"
    runtime = report["metrics"]["runtime_attestation"]
    assert runtime["mode"] == "component_script_isolated_v1"
    assert runtime["cli_sha256"] == hashlib.sha256(
        (project / "validator" / "src" / "wikidebia_validator" / "cli.py").read_bytes()
    ).hexdigest()
    assert runtime["editorial_sha256"] == hashlib.sha256(
        (project / "validator" / "src" / "wikidebia_validator" / "editorial.py").read_bytes()
    ).hexdigest()
    assert not (project / "outgoing").exists()
