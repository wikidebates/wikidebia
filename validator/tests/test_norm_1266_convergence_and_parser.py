from __future__ import annotations
import hashlib
import json
from pathlib import Path

from wikidebia_validator.editorial import _validate_semantic_convergence
from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report
from wikidebia_validator.wikicode import parse_template


def _canon_sha(obj: dict, omitted: str) -> str:
    data = dict(obj); data.pop(omitted, None)
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def test_multiline_summary_and_quote_are_parsed_as_complete_values():
    text = '''{{Argument
|summary=First line of the summary.
Second line with {{Wikipedia link|article=Evidence}} and a | character inside [https://example.org label].
Third line completes the reasoning.
|quotes={{Quote
|quote=First line of the quotation.
Second line of the quotation.
|authors=Author
|date=2020
}}
|sections=Philosophy
|keywords=evidence, reasoning
|creation-date=2026-08-10
}}'''
    tmpl = parse_template(text)
    assert "Second line with" in (tmpl.one("summary") or "")
    assert "Third line completes" in (tmpl.one("summary") or "")
    assert "Second line of the quotation" in (tmpl.one("quotes") or "")


def test_semantic_convergence_validator_accepts_two_distinct_clean_passes(tmp_path: Path):
    review = {
        "schema": "wikidebia-en-translation-review-1.1", "schema_version": "1.1",
        "status": "approved", "semantic_content_sha256": "a" * 64, "final_values": {},
        "review_sha256": None,
    }
    review["review_sha256"] = _canon_sha(review, "review_sha256")
    receipt = {
        "schema": "wikidebia-semantic-convergence-review-1.0", "schema_version": "1.0",
        "translation_review_sha256": review["review_sha256"], "semantic_content_sha256": review["semantic_content_sha256"],
        "status": "converged", "passes": [
            {"method":"proposition comparison", "new_certain_errors":0, "translation_review_sha256":review["review_sha256"], "semantic_content_sha256":review["semantic_content_sha256"]},
            {"method":"risk-marker reread", "new_certain_errors":0, "translation_review_sha256":review["review_sha256"], "semantic_content_sha256":review["semantic_content_sha256"]},
        ], "receipt_sha256": None,
    }
    receipt["receipt_sha256"] = _canon_sha(receipt, "receipt_sha256")
    (tmp_path / "reviews/en").mkdir(parents=True)
    (tmp_path / "reviews/en/translation_review.json").write_text(json.dumps(review), encoding="utf-8")
    (tmp_path / "reviews/en/semantic_convergence_review.json").write_text(json.dumps(receipt), encoding="utf-8")
    manifest={"editorial_controls":{"translation_semantic_review_schema_version":"1.3","semantic_convergence_review_path":"reviews/en/semantic_convergence_review.json","semantic_convergence_review_schema_version":"1.0"},"translation_status":{"en":"ready"}}
    ctx=PackageContext(tmp_path, Report("0.4.69", str(tmp_path), ["editorial"]), cache={"manifest.json":manifest})
    metrics=_validate_semantic_convergence(ctx, manifest["editorial_controls"], False)
    assert metrics["status"] == "converged"
    assert not [f for f in ctx.report.findings if f.code == "WDV-BIL-009" and f.level == "ERROR"]


def test_semantic_convergence_validator_rejects_same_method(tmp_path: Path):
    review={"schema":"wikidebia-en-translation-review-1.1","schema_version":"1.1","status":"approved","semantic_content_sha256":"b"*64,"review_sha256":None}
    review["review_sha256"]=_canon_sha(review,"review_sha256")
    row={"method":"same method repeated","new_certain_errors":0,"translation_review_sha256":review["review_sha256"],"semantic_content_sha256":review["semantic_content_sha256"]}
    receipt={"schema":"wikidebia-semantic-convergence-review-1.0","schema_version":"1.0","translation_review_sha256":review["review_sha256"],"semantic_content_sha256":review["semantic_content_sha256"],"status":"converged","passes":[dict(row),dict(row)],"receipt_sha256":None}
    receipt["receipt_sha256"]=_canon_sha(receipt,"receipt_sha256")
    (tmp_path/"reviews/en").mkdir(parents=True)
    (tmp_path/"reviews/en/translation_review.json").write_text(json.dumps(review),encoding="utf-8")
    (tmp_path/"reviews/en/semantic_convergence_review.json").write_text(json.dumps(receipt),encoding="utf-8")
    manifest={"editorial_controls":{"translation_semantic_review_schema_version":"1.3","semantic_convergence_review_path":"reviews/en/semantic_convergence_review.json","semantic_convergence_review_schema_version":"1.0"},"translation_status":{"en":"ready"}}
    ctx=PackageContext(tmp_path, Report("0.4.69", str(tmp_path), ["editorial"]), cache={"manifest.json":manifest})
    _validate_semantic_convergence(ctx, manifest["editorial_controls"], False)
    assert any(f.code == "WDV-BIL-009" and f.level == "ERROR" for f in ctx.report.findings)
