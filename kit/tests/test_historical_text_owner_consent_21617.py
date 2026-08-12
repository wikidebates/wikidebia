from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import wikidebia_content_review as content
import wikidebia_review_workflow as workflow


def _review(*, intro_final: str | None = None, summary_final: str | None = None, with_requests: bool = True) -> dict:
    intro_old = "{{Sous-partie|titre=Contexte|contenu=Texte historique.<references />}}"
    summary_old = "Résumé historique avec une coquile."
    debate_review = {
        "historical_text_policy": content.HISTORICAL_TEXT_POLICY,
        "historical_text_status": "preserved",
        "introduction_decision": "keep",
        "proposed_introduction": intro_old,
        "suggested_change": None,
        "historical_change_request": None,
    }
    arg_review = {
        "historical_text_policy": content.HISTORICAL_TEXT_POLICY,
        "historical_text_status": "preserved",
        "historical_summary_present": True,
        "historical_summary_sha256": content._historical_text_sha256(summary_old),
        "summary_decision": "keep",
        "proposed_summary": summary_old,
        "suggested_change": None,
        "historical_change_request": None,
    }
    if intro_final is not None:
        debate_review.update({"historical_text_status":"authorization_requested","introduction_decision":"change","proposed_introduction":intro_final})
        if with_requests:
            debate_review["historical_change_request"] = {
                "field_key":"debate:debat_test:introduction","final_value":intro_final,"change_type":"mediawiki_syntax",
                "rationale":"Suppression explicitement demandée de la balise MediaWiki obsolète.","owner_instruction_reference":"owner-msg-1",
            }
    if summary_final is not None:
        arg_review.update({"historical_text_status":"authorization_requested","summary_decision":"change","proposed_summary":summary_final})
        if with_requests:
            arg_review["historical_change_request"] = {
                "field_key":"argument:A0001:summary","final_value":summary_final,"change_type":"typo",
                "rationale":"Correction locale explicitement approuvée par le propriétaire.","owner_instruction_reference":"owner-msg-1",
            }
    return {
        "schema": content.CONTENT_REVIEW_SCHEMA, "schema_version":"1.1", "debate_id":"debat_test", "work_id":"EDIT-1",
        "debate":{"source":{"page_origin":"preexisting","introduction":intro_old},"review":debate_review},
        "arguments":[{"id":"A0001","source":{"id":"A0001","page_origin":"preexisting","summary":summary_old},"review":arg_review}],
    }


def _manifest() -> dict:
    return {
        "review_type":"fr_content_review", "package_id":"pkg-1", "manifest_sha256":"a"*64,
        "editable_files":[{"package_path":"editable/reviews/fr/content_review.json","target_path":"reviews/fr/content_review.json"}],
    }


def test_owner_consent_flag_is_required_for_requested_historical_delta(tmp_path: Path):
    review = _review(summary_final="Résumé historique avec une coquille.")
    files={"editable/reviews/fr/content_review.json": (json.dumps(review, ensure_ascii=False)+"\n").encode()}
    archive=tmp_path/"returned.zip"; archive.write_bytes(b"returned-review")
    with pytest.raises(workflow.WorkflowError, match="consentement explicite"):
        workflow._prepare_historical_consent_import(archive,{"debate_id":"debat_test","work_id":"EDIT-1"},_manifest(),files,authorize_historical_changes=False)


def test_owner_consent_flag_creates_non_zip_scoped_authorization(tmp_path: Path):
    review = _review(summary_final="Résumé historique avec une coquille.")
    files={"editable/reviews/fr/content_review.json": (json.dumps(review, ensure_ascii=False)+"\n").encode()}
    archive=tmp_path/"returned.zip"; archive.write_bytes(b"returned-review")
    _, normalized, auth = workflow._prepare_historical_consent_import(archive,{"debate_id":"debat_test","work_id":"EDIT-1"},_manifest(),files,authorize_historical_changes=True)
    assert normalized is not None and auth is not None
    assert auth["authorization_method"] == "owner_explicit_cli_flag"
    assert auth["returned_archive_sha256"] == workflow._sha256_file(archive)
    assert [x["field_key"] for x in auth["changes"]] == ["argument:A0001:summary"]
    assert "authorization_id" not in json.dumps(normalized)


def test_owner_applies_multiple_proposed_changes_in_one_scoped_consent(tmp_path: Path):
    intro="{{Sous-partie|titre=Contexte|contenu=Texte historique.}}"
    review=_review(intro_final=intro, summary_final="Résumé historique avec une coquille.")
    files={"editable/reviews/fr/content_review.json": (json.dumps(review, ensure_ascii=False)+"\n").encode()}
    archive=tmp_path/"returned.zip"; archive.write_bytes(b"same-exact-return")
    _, _, auth=workflow._prepare_historical_consent_import(archive,{"debate_id":"debat_test","work_id":"EDIT-1"},_manifest(),files,authorize_historical_changes=True)
    assert auth is not None
    assert {x["field_key"] for x in auth["changes"]} == {"debate:debat_test:introduction","argument:A0001:summary"}


def test_arbitrary_delta_without_structured_request_is_blocked_before_consent(tmp_path: Path):
    review=_review(summary_final="Modification arbitraire.", with_requests=False)
    files={"editable/reviews/fr/content_review.json": (json.dumps(review, ensure_ascii=False)+"\n").encode()}
    archive=tmp_path/"returned.zip"; archive.write_bytes(b"x")
    with pytest.raises(workflow.WorkflowError, match="résumé historique"):
        workflow._prepare_historical_consent_import(archive,{"debate_id":"debat_test","work_id":"EDIT-1"},_manifest(),files,authorize_historical_changes=True)


def test_authorization_flag_without_any_historical_delta_is_rejected(tmp_path: Path):
    review=_review()
    files={"editable/reviews/fr/content_review.json": (json.dumps(review, ensure_ascii=False)+"\n").encode()}
    archive=tmp_path/"returned.zip"; archive.write_bytes(b"x")
    with pytest.raises(workflow.WorkflowError, match="rien à autoriser"):
        workflow._prepare_historical_consent_import(archive,{"debate_id":"debat_test","work_id":"EDIT-1"},_manifest(),files,authorize_historical_changes=True)


def test_legacy_21614_delta_is_migrated_to_suggestion_without_redoing_review(tmp_path: Path):
    legacy=_review(summary_final="Ancienne proposition de réécriture.", with_requests=False)
    # Remove all consent-aware markers to emulate a pre-1.2.83 payload.
    rev=legacy["arguments"][0]["review"]
    for key in ("historical_text_policy","historical_text_status","historical_summary_present","historical_summary_sha256","suggested_change","historical_change_request"):
        rev.pop(key,None)
    files={"editable/reviews/fr/content_review.json": (json.dumps(legacy, ensure_ascii=False)+"\n").encode()}
    archive=tmp_path/"returned.zip"; archive.write_bytes(b"legacy")
    normalized_files, normalized, auth=workflow._prepare_historical_consent_import(archive,{"debate_id":"debat_test","work_id":"EDIT-1"},_manifest(),files,authorize_historical_changes=False)
    assert auth is None and normalized is not None
    rev2=normalized["arguments"][0]["review"]
    assert rev2["summary_decision"] == "keep"
    assert rev2["suggested_change"]["value"] == "Ancienne proposition de réécriture."
    assert "compatibility_migration" in normalized
    assert normalized_files["editable/reviews/fr/content_review.json"]


def test_review_package_without_content_review_payload_keeps_legacy_orchestration_compatible(tmp_path: Path):
    archive=tmp_path/"returned.zip"; archive.write_bytes(b"x")
    manifest={"review_type":"fr_content_review","editable_files":[{"package_path":"editable/reviews/edit.json","target_path":"reviews/edit.json"}]}
    files={"editable/reviews/edit.json":b"{}\n"}
    same, normalized, auth=workflow._prepare_historical_consent_import(archive,{"debate_id":"debat_test","work_id":"EDIT-1"},manifest,files,authorize_historical_changes=False)
    assert same == files and normalized is None and auth is None
