from __future__ import annotations

import importlib.util
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "wikidebia_manage.py"
spec = importlib.util.spec_from_file_location("wikidebia_manage_mode_repair", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_historical_direct_entrypoints_remain_executable():
    # Managers prior to 2.15.2 extracted ZIP contents with Python zipfile, which
    # discarded Unix modes.  The staged test run repairs that migration case
    # before the component is atomically installed.
    module.restore_historical_entrypoint_modes(ROOT)
    for rel in ("scripts/wikidebia_graph_extract.py", "scripts/wikidebia_corpus_init.py"):
        mode = stat.S_IMODE((ROOT / rel).stat().st_mode)
        assert mode & 0o111, rel
