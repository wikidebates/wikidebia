"""Test bootstrap shared by every pytest process.

Operational scripts are executable siblings under ``scripts/`` and import the
central release metadata module from that directory.  Full-suite runs put this
path in ``sys.path`` indirectly through earlier imports, which hid an order
and isolation dependency.  Make the test environment explicit instead.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
