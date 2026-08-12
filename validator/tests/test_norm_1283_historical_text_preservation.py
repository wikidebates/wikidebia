from __future__ import annotations

import hashlib
import json
from pathlib import Path

from wikidebia_validator.editorial import validate_introduction_review_data
from wikidebia_validator.validator import validate_package
from wikidebia_validator.wikicode import parse_template
from .helpers import create_fr_package, dump


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _attach_preservation_lock(root: Path) -> tuple[dict, dict[str, str]]:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    debate_page = next(p for p in manifest["pages"] if p["language"] == "fr" and p["page_type"] == "debate")
    arg_pages = [p for p in manifest["pages"] if p["language"] == "fr" and p["page_type"] == "argument"]
    debate = parse_template((root / debate_page["file_path"]).read_text(encoding="utf-8"))
    intro = debate.one("introduction") or ""
    summaries: dict[str, str] = {}
    rows = []
    for page in arg_pages:
        tmpl = parse_template((root / page["file_path"]).read_text(encoding="utf-8"))
        summary = tmpl.one("résumé") or ""
        summaries[page["page_id"]] = summary
        rows.append({
            "id": page["page_id"],
            "page_origin": "preexisting",
            "summary_provenance": "historical_existing" if summary else "historical_absent",
            "source_sha256": _sha(summary),
            "preserved": True,
        })
    dump(root / "data/fr_content_lock.json", {
        "historical_text_preservation": {
            "policy": "preserve_preexisting_exact_v1",
            "debate": {
                "page_origin": "preexisting",
                "introduction_provenance": "historical_existing" if intro else "historical_absent",
                "source_sha256": _sha(intro),
                "preserved": True,
            },
            "arguments": rows,
        }
    })
    return debate_page, {"introduction": intro, **summaries}


def test_historical_text_lock_accepts_exact_rendered_values(tmp_path: Path):
    create_fr_package(tmp_path)
    _attach_preservation_lock(tmp_path)
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert not any(f.code == "WDV-EDT-034" for f in report.findings)


def test_historical_text_lock_blocks_summary_rewrite(tmp_path: Path):
    create_fr_package(tmp_path)
    _attach_preservation_lock(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    page = next(p for p in manifest["pages"] if p["language"] == "fr" and p["page_id"] == "A0001")
    path = tmp_path / page["file_path"]
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("La mesure X mutualiserait certains bénéfices et réduirait des coûts collectifs.", "Résumé réécrit qui ne doit pas passer."), encoding="utf-8")
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.code == "WDV-EDT-034" and "Résumé historique" in f.message for f in report.findings)


def test_historical_text_lock_blocks_introduction_rewrite(tmp_path: Path):
    create_fr_package(tmp_path)
    debate_page, _ = _attach_preservation_lock(tmp_path)
    path = tmp_path / debate_page["file_path"]
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("La mesure X est une mesure pilote.", "Une nouvelle introduction réécrite."), encoding="utf-8")
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.code == "WDV-EDT-034" and "Introduction historique" in f.message for f in report.findings)


def test_historical_introduction_review_skips_creation_structure_requirements():
    intro = "{{Sous-partie|titre=Historique|contenu=Texte historique conservé.}}"
    review = {
        "entries": [{
            "language": "fr",
            "status": "historical_existing",
            "historical_content_preserved": True,
            "historical_source_sha256": _sha(intro),
            "note": "Introduction historique conservée exactement sans réécriture rétroactive.",
            "subsections": [{"title": "Historique"}],
        }]
    }
    issues = validate_introduction_review_data(review, {"fr": ["Historique"]})
    assert issues == []

def test_summary_style_schema_accepts_translated_historical_source():
    import json
    from pathlib import Path
    schema = json.loads((Path(__file__).resolve().parents[1] / "src/wikidebia_validator/schemas/summary_style_review.schema.json").read_text(encoding="utf-8"))
    variants = schema["properties"]["entries"]["items"]["properties"]["languages"]["patternProperties"]["^(fr|en)$"]["oneOf"]
    assert any(v.get("properties", {}).get("status", {}).get("const") == "translated_historical_source" for v in variants)

def test_summary_style_allows_english_translation_of_protected_historical_source():
    from wikidebia_validator.editorial import validate_summary_style_review_data
    review = {
        "entries": [{
            "id": "A0001",
            "languages": {
                "fr": {"status": "historical_existing", "historical_content_preserved": True, "note": "Résumé français historique conservé exactement."},
                "en": {"status": "translated_historical_source", "historical_source_preserved": True, "note": "English faithfully translates the protected historical French source."},
            },
        }]
    }
    issues = validate_summary_style_review_data(
        review,
        [{"id": "A0001"}],
        {"A0001": {"fr", "en"}},
        protected_historical={("A0001", "fr")},
        summaries={("A0001", "fr"): "A", ("A0001", "en"): "A"},
    )
    assert issues == []



def _canonical_sha(obj: dict) -> str:
    import copy
    body = copy.deepcopy(obj)
    body.pop("authorization_sha256", None)
    return hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _attach_consent_lock(root: Path, *, authorize_summary: bool = False, authorize_intro: bool = False) -> tuple[dict, dict[str, str]]:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    debate_page = next(p for p in manifest["pages"] if p["language"] == "fr" and p["page_type"] == "debate")
    arg_pages = [p for p in manifest["pages"] if p["language"] == "fr" and p["page_type"] == "argument"]
    debate_t = parse_template((root / debate_page["file_path"]).read_text(encoding="utf-8"))
    intro = debate_t.one("introduction") or ""
    rows=[]; summaries={}; auth_changes=[]; auth_id="AUTH-TEST"
    debate_final = intro
    debate_decision = "preserved"
    debate_auth = None
    if authorize_intro:
        debate_final = intro + " {{Sous-partie|titre=Enjeux du débat|contenu=Ajout explicitement autorisé.}}"
        path=root/debate_page["file_path"]
        text=path.read_text(encoding="utf-8")
        text=text.replace(f"|introduction={intro}", f"|introduction={debate_final}", 1)
        path.write_text(text, encoding="utf-8")
        debate_decision="authorized_change"
        debate_auth={"authorization_id":auth_id,"historical_sha256":_sha(intro),"final_sha256":_sha(debate_final)}
        auth_changes.append({"field_key":f"debate:{manifest['debate_id']}:introduction",**debate_auth,"change_type":"structure"})
    for page in arg_pages:
        tmpl=parse_template((root/page["file_path"]).read_text(encoding="utf-8")); summary=tmpl.one("résumé") or ""; summaries[page["page_id"]]=summary
        final=summary; decision="preserved"; auth=None
        if authorize_summary and page["page_id"]=="A0001":
            final=summary + " Correction autorisée."
            path=root/page["file_path"]; text=path.read_text(encoding="utf-8"); text=text.replace(f"|résumé={summary}", f"|résumé={final}",1); path.write_text(text,encoding="utf-8")
            decision="authorized_change"; auth={"authorization_id":auth_id,"historical_sha256":_sha(summary),"final_sha256":_sha(final)}
            auth_changes.append({"field_key":"argument:A0001:summary",**auth,"change_type":"typo"})
        rows.append({"id":page["page_id"],"field_key":f"argument:{page['page_id']}:summary","page_origin":"preexisting","historical_status":"historical_existing" if summary else "historical_absent","historical_present":bool(summary),"historical_sha256":_sha(summary),"final_present":bool(final),"final_sha256":_sha(final),"decision":decision,"authorization":auth})
    receipt_path=None; receipt_sha=None
    if auth_changes:
        receipt={"schema":"wikidebia-owner-historical-text-authorization-1.0","schema_version":"1.0","authorization_id":auth_id,"debate_id":manifest["debate_id"],"work_id":"EDIT-TEST","changes":auth_changes,"authorization_sha256":None}
        receipt["authorization_sha256"]=_canonical_sha(receipt)
        receipt_path="reviews/fr/historical_text_authorization.json"; dump(root/receipt_path,receipt); receipt_sha=hashlib.sha256((root/receipt_path).read_bytes()).hexdigest()
    dump(root/"data/fr_content_lock.json", {
        "debate_id":manifest["debate_id"],"work_id":"EDIT-TEST",
        "historical_text_decisions":{
            "policy":"preserve_by_default_owner_authorized_v2","authorization_receipt_path":receipt_path,"authorization_receipt_sha256":receipt_sha,
            "debate":{"field_key":f"debate:{manifest['debate_id']}:introduction","page_origin":"preexisting","historical_status":"historical_existing" if intro else "historical_absent","historical_present":bool(intro),"historical_sha256":_sha(intro),"final_present":bool(debate_final),"final_sha256":_sha(debate_final),"decision":debate_decision,"authorization":debate_auth},
            "arguments":rows,
        }
    })
    return debate_page,{"introduction":intro,**summaries}


def test_consent_lock_preserved_mode_accepts_identity(tmp_path: Path):
    create_fr_package(tmp_path); _attach_consent_lock(tmp_path)
    report=validate_package(tmp_path,scopes=["wikicode"])
    assert not any(f.code=="WDV-EDT-034" for f in report.findings)


def test_consent_lock_authorized_summary_change_accepts_exact_receipt_and_render(tmp_path: Path):
    create_fr_package(tmp_path); _attach_consent_lock(tmp_path,authorize_summary=True)
    report=validate_package(tmp_path,scopes=["wikicode"])
    assert not any(f.code=="WDV-EDT-034" for f in report.findings)


def test_consent_lock_forged_authorized_change_without_receipt_is_blocked(tmp_path: Path):
    create_fr_package(tmp_path); _attach_consent_lock(tmp_path)
    lock=json.loads((tmp_path/"data/fr_content_lock.json").read_text()); row=lock["historical_text_decisions"]["arguments"][0]
    row["decision"]="authorized_change"; row["authorization"]={"authorization_id":"FAKE","historical_sha256":row["historical_sha256"],"final_sha256":row["final_sha256"]}
    dump(tmp_path/"data/fr_content_lock.json",lock)
    report=validate_package(tmp_path,scopes=["wikicode"])
    assert any(f.code=="WDV-EDT-034" and ("reçu" in f.message.lower() or "preuve" in f.message.lower()) for f in report.findings)


def test_consent_lock_authorized_final_hash_mismatch_is_blocked(tmp_path: Path):
    create_fr_package(tmp_path); _attach_consent_lock(tmp_path,authorize_summary=True)
    manifest=json.loads((tmp_path/"manifest.json").read_text()); page=next(p for p in manifest["pages"] if p.get("page_id")=="A0001" and p["language"]=="fr")
    path=tmp_path/page["file_path"]; path.write_text(path.read_text().replace(" Correction autorisée."," Altération parasite."),encoding="utf-8")
    report=validate_package(tmp_path,scopes=["wikicode"])
    assert any(f.code=="WDV-EDT-034" and "valeur finale autorisée" in f.message for f in report.findings)


def test_consent_lock_authorized_introduction_change_is_accepted(tmp_path: Path):
    create_fr_package(tmp_path); _attach_consent_lock(tmp_path,authorize_intro=True)
    report=validate_package(tmp_path,scopes=["wikicode"])
    assert not any(f.code=="WDV-EDT-034" for f in report.findings)


def test_consent_lock_historical_absence_cannot_be_created_while_preserved(tmp_path: Path):
    create_fr_package(tmp_path); _attach_consent_lock(tmp_path)
    lock=json.loads((tmp_path/"data/fr_content_lock.json").read_text()); row=lock["historical_text_decisions"]["arguments"][0]
    row["historical_status"]="historical_absent"; row["historical_present"]=False; row["historical_sha256"]=_sha(""); row["final_sha256"]=_sha(""); row["final_present"]=False
    dump(tmp_path/"data/fr_content_lock.json",lock)
    report=validate_package(tmp_path,scopes=["wikicode"])
    assert any(f.code=="WDV-EDT-034" for f in report.findings)


def _upgrade_consent_lock_to_v3_scope(root: Path, field_key: str, scope: dict) -> None:
    lock_path=root/"data/fr_content_lock.json"
    lock=json.loads(lock_path.read_text(encoding="utf-8"))
    decisions=lock["historical_text_decisions"]
    decisions["policy"]="preserve_by_default_owner_authorized_v3"
    if field_key.startswith("debate:"):
        row=decisions["debate"]
    else:
        page_id=field_key.split(":",2)[1]
        row=next(x for x in decisions["arguments"] if x["id"]==page_id)
    row["change_scope"]=scope
    receipt_path=decisions.get("authorization_receipt_path")
    if receipt_path:
        receipt=json.loads((root/receipt_path).read_text(encoding="utf-8"))
        rr=next(x for x in receipt["changes"] if x["field_key"]==field_key)
        rr["change_scope"]=scope
        if isinstance(row.get("authorization"),dict):
            row["authorization"]["change_scope"]=scope
            row["authorization"]["change_type"]=rr.get("change_type")
        receipt["authorization_sha256"]=_canonical_sha(receipt)
        dump(root/receipt_path,receipt)
        decisions["authorization_receipt_sha256"]=hashlib.sha256((root/receipt_path).read_bytes()).hexdigest()
    dump(lock_path,lock)


def test_consent_v3_authorized_introduction_requires_matching_structured_scope(tmp_path: Path):
    create_fr_package(tmp_path); debate_page,_=_attach_consent_lock(tmp_path,authorize_intro=True)
    field_key=f"debate:{json.loads((tmp_path/'manifest.json').read_text())['debate_id']}:introduction"
    scope={
        "mode":"subsections",
        "historical_titles":["Contexte"],
        "final_titles":["Contexte","Enjeux du débat"],
        "added":[{"title":"Enjeux du débat","occurrence":1}],
        "modified":[],"removed":[],"reordered":False,
    }
    _upgrade_consent_lock_to_v3_scope(tmp_path,field_key,scope)
    report=validate_package(tmp_path,scopes=["wikicode"])
    assert not any(f.code=="WDV-EDT-034" for f in report.findings)

    lock=json.loads((tmp_path/"data/fr_content_lock.json").read_text())
    lock["historical_text_decisions"]["debate"]["change_scope"]={"mode":"whole_field"}
    dump(tmp_path/"data/fr_content_lock.json",lock)
    report=validate_package(tmp_path,scopes=["wikicode"])
    assert any(f.code=="WDV-EDT-034" and "Portée" in f.message for f in report.findings)
