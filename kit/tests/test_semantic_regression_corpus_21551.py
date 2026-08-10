from __future__ import annotations
import json, sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import wikidebia_translation_review as translation  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "translation_semantic_real_cases_1.0.json"


def test_real_translation_regression_corpus_bad_and_good_pairs():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["schema"] == "wikidebia-real-translation-regressions-1.0"
    assert len(data["cases"]) >= 12
    for case in data["cases"]:
        bad = set(translation._semantic_risk_signals(case["fr"], case["bad_en"]))
        good = set(translation._semantic_risk_signals(case["fr"], case["good_en"]))
        for expected in case["expected"]:
            assert expected in bad, (case["id"], expected, bad)
            assert expected not in good, (case["id"], expected, good)


def test_kit_semantic_marker_labels_match_current_validator_catalog_when_siblings_present():
    validator_src = Path(__file__).resolve().parents[2] / "validator" / "src"
    if not validator_src.exists():
        # The kit remains testable alone; the release integration suite runs this
        # contract again with the three current components side-by-side.
        return
    sys.path.insert(0, str(validator_src))
    from wikidebia_validator.editorial import SEMANTIC_MARKERS  # type: ignore
    assert set(translation.SEMANTIC_RISK_MARKERS) == set(SEMANTIC_MARKERS)
