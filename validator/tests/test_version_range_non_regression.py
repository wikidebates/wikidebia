from pathlib import Path


def test_active_sources_do_not_skip_1215_1216_before_1217():
    root = Path(__file__).resolve().parents[1] / "src" / "wikidebia_validator"
    combined = "\n".join(p.read_text(encoding="utf-8") for p in root.glob("*.py"))
    assert '"1.2.14", "1.2.17"' not in combined


def test_active_rule_sets_include_current_revision():
    root = Path(__file__).resolve().parents[1] / "src" / "wikidebia_validator"
    files = ["coherence.py", "validator.py", "sources.py", "workflow.py", "bilingual.py", "files.py", "graph.py", "editorial.py", "batches.py"]
    for name in files:
        text = (root / name).read_text(encoding="utf-8")
        assert "1.2.21" in text, name
