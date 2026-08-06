from pathlib import Path
import hashlib, json

from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package, dump


def _field(text, name):
    start=text.index("|"+name+"=")+len(name)+2
    end=text.find("\n|",start)
    return text[start:end]


def _package(root:Path):
    create_fr_package(root)
    manifest=json.loads((root/"manifest.json").read_text())
    manifest["translation_status"]={"en":"deferred"}
    manifest["editorial_controls"]={
      "creation_date":"2026-07-23","creation_date_policy":"per_page_preserved",
      "individual_review_path":"reviews/individual_review.json","individual_review_report_path":"reports/individual.txt",
      "keyword_vocabulary_path":"data/keyword_vocabulary.json","summary_style_review_path":"reviews/summary_style_review.json",
      "required_reports":[],"debate_documentation":{"min_subsections":1,"min_references":0,"reject_singleton_bucket_pattern":True,"profile_rationale":"Profil de test complet."},
      "introduction_references":{"required":True},"introduction_review_path":"reviews/introduction_review.json",
      "graph_placement_review_path":"reviews/graph_placement_review.json","keyword_policy_revision":"1.2.39",
      "legacy_content_preservation":{"enabled":True,"lock_path":"data/historical_content_lock.json","protected_fields":["résumé","initialisation"],"source_archive_sha256":"a"*64}
    }
    dump(root/"manifest.json",manifest)
    page=manifest["pages"][1]
    path=root/page["file_path"]
    text=path.read_text()
    text=text.replace("{{Argument\n","{{Argument\n|initialisation=Objection@42\n",1)
    path.write_text(text)
    summary=_field(text,"résumé")
    dump(root/"data/historical_content_lock.json",{"schema_version":"1.0","debate_id":manifest["debate_id"],"source_archive":"source.zip","source_archive_sha256":"a"*64,"protected_fields":["résumé","initialisation"],"arguments":[{"id":page["page_id"],"language":"fr","summary_provenance":"historical_existing","summary_sha256":hashlib.sha256(summary.encode()).hexdigest(),"summary_length":len(summary),"initialisation":{"present":True,"value":"Objection@42"}}]})
    vocab={"status":"draft","keyword_policy_revision":"1.2.39","entries":[{"fr":"mesure X","en":None,"kind":"noun_phrase","scope":"site_navigation","cross_debate_reusable":True,"local_frequency_is_validity_criterion":False,"usage_count_in_debate":2,"atomic_concept":True,"compositional_intersection":False,"multiword_exception":False}]}
    dump(root/"data/keyword_vocabulary.json",vocab)
    return manifest,page,path


def test_keyword_only_policy_does_not_activate_summary_or_capitalization(tmp_path:Path):
    manifest,page,path=_package(tmp_path)
    text=path.read_text().replace(_field(path.read_text(),"résumé"),"La thèse en tire une conséquence directe pour dieu.")
    path.write_text(text)
    # Adjust lock because this test is about policy separation, not content preservation.
    lock=json.loads((tmp_path/"data/historical_content_lock.json").read_text());summary=_field(text,"résumé");lock["arguments"][0]["summary_sha256"]=hashlib.sha256(summary.encode()).hexdigest();lock["arguments"][0]["summary_length"]=len(summary);dump(tmp_path/"data/historical_content_lock.json",lock)
    report=validate_package(tmp_path,scopes=["editorial","wikicode","schema"] )
    assert not any(f.code in {"WDV-EDT-024","WDV-EDT-026"} for f in report.findings)


def test_historical_summary_change_is_blocked(tmp_path:Path):
    manifest,page,path=_package(tmp_path)
    path.write_text(path.read_text().replace(_field(path.read_text(),"résumé"),"Résumé remplacé sans autorisation."))
    report=validate_package(tmp_path,scopes=["wikicode"] )
    assert any(f.code=="WDV-EDT-027" and "Résumé" in f.message for f in report.findings)


def test_historical_initialisation_removal_is_blocked(tmp_path:Path):
    manifest,page,path=_package(tmp_path)
    path.write_text(path.read_text().replace("|initialisation=Objection@42\n",""))
    report=validate_package(tmp_path,scopes=["wikicode"] )
    assert any(f.code=="WDV-EDT-027" and "initialisation" in f.message for f in report.findings)


def test_initialisation_on_unlocked_new_page_is_blocked(tmp_path:Path):
    manifest,page,path=_package(tmp_path)
    other=manifest["pages"][2];other_path=tmp_path/other["file_path"];other_path.write_text(other_path.read_text().replace("{{Argument\n","{{Argument\n|initialisation=Justification@9\n",1))
    report=validate_package(tmp_path,scopes=["wikicode"] )
    assert any(f.code=="WDV-EDT-027" and f.details.get("page_id")==other["page_id"] for f in report.findings)


def test_generated_after_import_summary_is_not_locked(tmp_path:Path):
    manifest,page,path=_package(tmp_path)
    lock=json.loads((tmp_path/"data/historical_content_lock.json").read_text())
    entry=lock["arguments"][0]
    entry["summary_provenance"]="generated_after_import"
    entry.pop("summary_sha256",None)
    entry.pop("summary_length",None)
    dump(tmp_path/"data/historical_content_lock.json",lock)
    path.write_text(path.read_text().replace(_field(path.read_text(),"résumé"),"Résumé généré après import et modifiable."))
    report=validate_package(tmp_path,scopes=["wikicode","schema"])
    assert not any(f.code=="WDV-EDT-027" and "Résumé historique" in f.message for f in report.findings)


def test_protected_historical_summary_is_exempt_from_retroactive_quality_rewrite(tmp_path:Path):
    manifest,page,path=_package(tmp_path)
    text=path.read_text().replace(_field(path.read_text(),"résumé"),"Texte historique {{Note|source ancienne}}. Cependant, cet argument peut être contesté.")
    path.write_text(text)
    from wikidebia_validator.wikicode import parse_template
    summary=parse_template(text).one("résumé")
    lock=json.loads((tmp_path/"data/historical_content_lock.json").read_text())
    lock["arguments"][0]["summary_sha256"]=hashlib.sha256(summary.encode()).hexdigest()
    lock["arguments"][0]["summary_length"]=len(summary)
    dump(tmp_path/"data/historical_content_lock.json",lock)
    report=validate_package(tmp_path,scopes=["wikicode","editorial","schema"])
    assert not any(f.code in {"WDV-MWK-020","WDV-EDT-003","WDV-EDT-013","WDV-EDT-014"} and f.path==page["file_path"] for f in report.findings)


def _enable_inventory_verification(root: Path, manifest: dict, page: dict, source_text: str):
    inventory_path = root / "data/initial_remote_inventory_fr.json"
    inventory = {
        "inventory_version": "1.0",
        "inventory_mode": "explicit_debate_pages_read_only",
        "debate_id": manifest["debate_id"],
        "language": "fr",
        "generated_at": "2026-08-06T00:00:00+00:00",
        "pages": [{
            "page_id": page["page_id"],
            "page_type": "argument",
            "canonical_title": page["canonical_title"],
            "content_sha256": hashlib.sha256(source_text.encode()).hexdigest(),
            "revision_id": 42,
            "status": "published",
            "content": source_text,
        }],
        "inventory_sha256": "0" * 64,
    }
    dump(inventory_path, inventory)
    manifest = json.loads((root / "manifest.json").read_text())
    cfg = manifest["editorial_controls"]["legacy_content_preservation"]
    cfg["verification_revision"] = "0.4.42"
    cfg["source_inventory_path"] = "data/initial_remote_inventory_fr.json"
    cfg["source_inventory_sha256"] = hashlib.sha256(inventory_path.read_bytes()).hexdigest()
    dump(root / "manifest.json", manifest)


def test_inventory_source_rejects_false_historical_summary(tmp_path: Path):
    manifest, page, path = _package(tmp_path)
    source_text = path.read_text()
    source_text = source_text.replace(f"|résumé={_field(source_text, 'résumé')}\n", "")
    _enable_inventory_verification(tmp_path, manifest, page, source_text)
    report = validate_package(tmp_path, scopes=["wikicode", "schema"])
    assert any(f.code == "WDV-EDT-027" and "absent de l’inventaire" in f.message for f in report.findings)


def test_inventory_source_rejects_missing_historical_initialisation(tmp_path: Path):
    manifest, page, path = _package(tmp_path)
    source_text = path.read_text()
    _enable_inventory_verification(tmp_path, manifest, page, source_text)
    lock = json.loads((tmp_path / "data/historical_content_lock.json").read_text())
    lock["arguments"][0]["initialisation"] = {"present": False}
    dump(tmp_path / "data/historical_content_lock.json", lock)
    path.write_text(path.read_text().replace("|initialisation=Objection@42\n", ""))
    report = validate_package(tmp_path, scopes=["wikicode", "schema"])
    assert any(f.code == "WDV-EDT-027" and "incohérent avec l’inventaire source" in f.message for f in report.findings)


def test_inventory_source_accepts_exact_historical_fields(tmp_path: Path):
    manifest, page, path = _package(tmp_path)
    _enable_inventory_verification(tmp_path, manifest, page, path.read_text())
    report = validate_package(tmp_path, scopes=["wikicode", "schema"])
    assert not any(f.code == "WDV-EDT-027" for f in report.findings)
