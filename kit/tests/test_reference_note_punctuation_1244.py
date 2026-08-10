import hashlib
import importlib.util
import sys
from pathlib import Path
import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "wikidebia_content_review.py"
spec = importlib.util.spec_from_file_location("content_review_1244", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_notice_without_terminal_period_needs_no_exception():
    intro = "Fait<ref>Jean Dupont, « Titre », 2012</ref>."
    assert module._validated_terminal_period_exceptions(intro, []) == []


def test_notice_with_terminal_period_is_rejected_without_sentence_attestation():
    intro = "Fait<ref>Jean Dupont, « Titre », 2012.</ref>."
    with pytest.raises(module.ContentReviewError):
        module._validated_terminal_period_exceptions(intro, [])


def test_complete_sentence_with_matching_exception_is_accepted():
    body = "Cette étude décrit précisément la méthode suivie."
    intro = f"Fait<ref>{body}</ref>."
    exception = {"body_sha256": hashlib.sha256(body.encode()).hexdigest(), "complete_sentence": True, "sentence_evidence": "décrit précisément la méthode"}
    assert module._validated_terminal_period_exceptions(intro, [exception]) == [exception]
