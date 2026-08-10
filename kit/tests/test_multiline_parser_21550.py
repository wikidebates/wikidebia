from __future__ import annotations
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from wikidebia_graph_extract import parse_template


def test_kit_parser_keeps_multiline_summary_and_quote_values_complete():
    raw='''{{Argument
|summary=First summary line.
Second summary line with {{Wikipedia link|article=Evidence}}.
Third summary line.
|quotes={{Quote
|quote=First quote line.
Second quote line.
|authors=Author
|date=2020
}}
|sections=Philosophy
|keywords=evidence, reasoning
|creation-date=2026-08-10
}}'''
    call=parse_template(raw)
    assert call is not None
    assert "Second summary line" in call.get("summary")
    assert "Third summary line" in call.get("summary")
    assert "Second quote line" in call.get("quotes")
