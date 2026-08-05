from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "wikidebia_update.py"
spec = importlib.util.spec_from_file_location("wikidebia_update_test", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)

TEST_VALIDATOR_PYTHON = "/usr/bin/python3" if Path("/usr/bin/python3").is_file() else sys.executable

MARKER = "|avertissements-argument=Argument généré par IA\n"


class FakeAdapter:
    def __init__(self, pages=None, rights=None):
        self.pages = dict(pages or {})
        self.rights = set(rights or {"edit", "createpage", "move", "delete", "browsearchive"})
        self.language = None
        self.next_revision = 100
        self.events = []
        self.fail_after_writes = None
        self.write_count = 0

    def open_language(self, language, expected_user):
        assert self.language is None
        self.language = language
        self.events.append(("open", language))

    def close_language(self):
        self.events.append(("close", self.language))
        self.language = None

    def assert_identity(self, expected_user):
        return None

    def user_rights(self):
        return set(self.rights)

    def read_page(self, title):
        row = self.pages.get((self.language, title))
        return (False, None, "") if row is None else (True, row[0], row[1])

    def write_page(self, *, title, text, summary, tags, expected_user, create_only, base_revision_id):
        if self.fail_after_writes is not None and self.write_count >= self.fail_after_writes:
            raise RuntimeError("interruption")
        key = (self.language, title)
        if create_only and key in self.pages:
            raise RuntimeError("create collision")
        if not create_only and (key not in self.pages or self.pages[key][0] != base_revision_id):
            raise RuntimeError("revision collision")
        self.next_revision += 1
        self.write_count += 1
        self.pages[key] = (self.next_revision, text)
        self.events.append(("write", self.language, title))
        return self.next_revision

    def move_page(self, *, old_title, new_title, reason, expected_user, leave_redirect):
        old = (self.language, old_title)
        new = (self.language, new_title)
        rev, text = self.pages.pop(old)
        self.next_revision += 1
        self.pages[new] = (self.next_revision, text)
        if leave_redirect:
            self.next_revision += 1
            self.pages[old] = (self.next_revision, module.redirect_text(self.language, new_title))
        self.events.append(("move", self.language, old_title, new_title))
        return self.next_revision

    def delete_page(self, *, title, reason, expected_user):
        self.pages.pop((self.language, title), None)
        self.events.append(("delete", self.language, title))

    def backlinks(self, title):
        return ["Page entrante"]


def argument(text: str) -> str:
    return "{{Argument\n" + MARKER + f"|résumé={text}\n|rubriques=Société\n}}}}\n"


def make_fixture(tmp_path: Path, *, languages=("fr",), old_pages=None, new_pages=None, migrations=None):
    root = tmp_path
    corpus = root / "corpus" / "demo"
    corpus.mkdir(parents=True)
    manifest_pages = []
    for language in languages:
        (corpus / "output" / language).mkdir(parents=True)
    for row in new_pages or []:
        language, page_id, title, text = row[:4]
        page_type = row[4] if len(row) > 4 else "argument"
        path = corpus / "output" / language / f"{page_id}.wiki"
        path.write_text(text, encoding="utf-8")
        manifest_pages.append({
            "language": language,
            "page_id": page_id,
            "page_type": page_type,
            "canonical_title": title,
            "file_path": path.relative_to(corpus).as_posix(),
            "sha256": module.sha_file(path),
        })
    manifest = {"debate_id": "demo", "release_version": "2026-07-31", "pages": manifest_pages}
    (corpus / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    if migrations:
        (corpus / "data").mkdir()
        (corpus / "data" / "remote_migrations.json").write_text(json.dumps({"version":"1.0","debate_id":"demo","entries":migrations}), encoding="utf-8")
    for language in languages:
        pages = []
        for row in old_pages or []:
            if row[0] != language:
                continue
            _, page_id, title, text = row[:4]
            page_type = row[4] if len(row) > 4 else "argument"
            revision = row[5] if len(row) > 5 else 10
            pages.append({"page_id": page_id, "page_type": page_type, "canonical_title": title, "content_sha256": module.sha_text(text), "revision_id": revision, "status":"published"})
        state = {"state_version":module.STATE_VERSION,"debate_id":"demo","language":language,"corpus_version":"old","publication_date":"2026-07-30T00:00:00Z","source_manifest_sha256":"0"*64,"plan_sha256":"1"*64,"pages":pages}
        state["state_sha256"] = module.sha_object(state)
        path = root / ".state" / "published" / "demo" / language / "latest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state), encoding="utf-8")
    validator = root / "validator.py"
    validator.write_text("import json; print(json.dumps({'validator_version':'0.4.37','result':'passed','summary':{'errors':0,'warnings':0}}))", encoding="utf-8")
    config = {
        "kit_version":"2.15.10","project_root":str(root),"debate_id":"demo","corpus_root":"corpus/demo","languages":list(languages),
        "family":"wikidebates","pywikibot_dir":"private/pywikibot","sites":{lang:{"code":lang,"expected_user":"ChatGPT"} for lang in languages},
        "validator":{"command":[TEST_VALIDATOR_PYTHON,str(validator),"validate"],"required_version":"0.4.37","scopes":[]},
        "published_state_dir":".state/published","receipts_dir":".state/receipts","logs_dir":"logs",
    }
    config_path = root / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return config, config_path


def plan(tmp_path, *, remote_pages=None, rights=None, **fixture):
    config, path = make_fixture(tmp_path, **fixture)
    adapter = FakeAdapter(remote_pages, rights)
    planner = module.RemoteUpdatePlanner(config, adapter, path)
    return planner.build_plan(), config, path, adapter


def test_01_new_page_is_create(tmp_path):
    p, *_ = plan(tmp_path, old_pages=[], new_pages=[("fr","A1","Titre",argument("Nouveau"))])
    assert p["counts"]["create"] == 1


def test_02_unchanged_page_is_skip(tmp_path):
    text = argument("Même")
    p, *_ = plan(tmp_path, old_pages=[("fr","A1","Titre",text)], new_pages=[("fr","A1","Titre",text)], remote_pages={("fr","Titre"):(10,text)})
    assert p["counts"]["skip"] == 1


def test_03_published_page_changed_in_corpus_is_update(tmp_path):
    old, new = argument("Ancien"), argument("Nouveau")
    p, *_ = plan(tmp_path, old_pages=[("fr","A1","Titre",old)], new_pages=[("fr","A1","Titre",new)], remote_pages={("fr","Titre"):(10,old)})
    assert p["counts"]["update"] == 1


def test_04_human_modified_page_is_manual_review(tmp_path):
    old, human, new = argument("Ancien"), argument("Modification humaine"), argument("Nouveau")
    p, *_ = plan(tmp_path, old_pages=[("fr","A1","Titre",old)], new_pages=[("fr","A1","Titre",new)], remote_pages={("fr","Titre"):(11,human)})
    assert p["counts"]["manual_review"] == 1
    assert p["comparisons"]


def test_05_removed_argument_is_delete(tmp_path):
    old = argument("Ancien")
    p, *_ = plan(tmp_path, old_pages=[("fr","A1","Titre",old)], new_pages=[("fr","A2","Conservé",argument("Présent"))], remote_pages={("fr","Titre"):(10,old),("fr","Conservé"):(20,argument("Présent"))})
    assert p["counts"]["delete"] == 1


def test_06_already_deleted_is_idempotent_skip(tmp_path):
    p, *_ = plan(tmp_path, old_pages=[("fr","A1","Titre",argument("Ancien"))], new_pages=[("fr","A2","Conservé",argument("Présent"))], remote_pages={("fr","Conservé"):(20,argument("Présent"))})
    assert any(row["page_id"] == "A1" for row in p["operations"]["skip"])


def test_07_renamed_argument_is_move(tmp_path):
    old, new = argument("Ancien"), argument("Nouveau")
    p, *_ = plan(tmp_path, old_pages=[("fr","A1","Ancien titre",old)], new_pages=[("fr","A1","Nouveau titre",new)], remote_pages={("fr","Ancien titre"):(10,old)})
    assert p["counts"]["move"] == 1


def test_08_merged_argument_can_redirect(tmp_path):
    old, target = argument("Fusionné"), argument("Cible")
    migrations=[{"language":"fr","old_page_id":"A1","kind":"merge","target_page_id":"A2","policy":"redirect"}]
    p, *_ = plan(tmp_path, old_pages=[("fr","A1","Ancien",old),("fr","A2","Cible",target)], new_pages=[("fr","A2","Cible",target)], migrations=migrations, remote_pages={("fr","Ancien"):(10,old),("fr","Cible"):(20,target)})
    assert p["counts"]["redirect"] == 1
    assert p["operations"]["redirect"][0]["backlinks"] == ["Page entrante"]


def test_09_never_published_page_is_not_deleted(tmp_path):
    p, *_ = plan(tmp_path, old_pages=[], new_pages=[("fr","A2","Conservé",argument("Présent"))], remote_pages={("fr","Étrangère"):(9,argument("Autre"))})
    assert p["counts"]["delete"] == 0


def test_10_page_owned_by_other_debate_is_blocked(tmp_path):
    old = argument("Ancien")
    p, config, path, adapter = plan(tmp_path, old_pages=[("fr","A1","Partagé",old)], new_pages=[("fr","A2","Conservé",argument("Présent"))], remote_pages={("fr","Partagé"):(10,old),("fr","Conservé"):(20,argument("Présent"))})
    other = {"state_version":module.STATE_VERSION,"debate_id":"autre","language":"fr","corpus_version":"x","publication_date":"x","source_manifest_sha256":"0"*64,"plan_sha256":"1"*64,"pages":[{"page_id":"Z","page_type":"argument","canonical_title":"Partagé","content_sha256":module.sha_text(old),"revision_id":10,"status":"published"}]}
    other["state_sha256"] = module.sha_object(other)
    op = tmp_path / ".state/published/autre/fr/latest.json"; op.parent.mkdir(parents=True); op.write_text(json.dumps(other),encoding="utf-8")
    p = module.RemoteUpdatePlanner(config, adapter, path).build_plan()
    assert p["counts"]["blocked"] == 1


def test_11_missing_delete_right_stops_before_write(tmp_path):
    old, kept = argument("Ancien"), argument("Présent")
    p, config, path, adapter = plan(tmp_path, rights={"edit","createpage"}, old_pages=[("fr","A1","Retiré",old),("fr","A2","Conservé",kept)], new_pages=[("fr","A2","Conservé",kept)], remote_pages={("fr","Retiré"):(10,old),("fr","Conservé"):(20,kept)})
    executor = module.PlanExecutor(config, adapter, path)
    try:
        executor.execute(p, p["plan_sha256"], only_delete=True)
    except module.PermissionDenied:
        pass
    else:
        raise AssertionError("delete sans droit accepté")
    assert not any(event[0] in {"write","delete","move"} for event in adapter.events)


def test_12_french_then_english_sessions_are_sequential(tmp_path):
    old_fr, old_en = argument("FR"), argument("EN")
    p, _, _, adapter = plan(tmp_path, languages=("fr","en"), old_pages=[("fr","A1","FR",old_fr),("en","A1","EN",old_en)], new_pages=[("fr","A1","FR",old_fr),("en","A1","EN",old_en)], remote_pages={("fr","FR"):(10,old_fr),("en","EN"):(11,old_en)})
    assert adapter.events[:4] == [("open","fr"),("close","fr"),("open","en"),("close","en")]


def test_13_interruption_then_resume_is_idempotent(tmp_path):
    one, two = argument("Un"), argument("Deux")
    p, config, path, adapter = plan(tmp_path, old_pages=[], new_pages=[("fr","A1","Un",one),("fr","A2","Deux",two)])
    executor = module.PlanExecutor(config, adapter, path)
    adapter.fail_after_writes = 1
    try:
        executor.execute(p, p["plan_sha256"])
    except RuntimeError:
        pass
    adapter.fail_after_writes = None
    receipt = executor.execute(p, p["plan_sha256"])
    assert receipt["counts"]["already_done"] == 1
    assert receipt["counts"]["created"] == 1


def test_14_remote_change_after_plan_is_conflict(tmp_path):
    old, new = argument("Ancien"), argument("Nouveau")
    p, config, path, adapter = plan(tmp_path, old_pages=[("fr","A1","Titre",old)], new_pages=[("fr","A1","Titre",new)], remote_pages={("fr","Titre"):(10,old)})
    adapter.pages[("fr","Titre")] = (11,argument("Changé après plan"))
    try:
        module.PlanExecutor(config, adapter, path).execute(p, p["plan_sha256"])
    except module.PlanConflict:
        pass
    else:
        raise AssertionError("conflit distant non détecté")


def test_15_only_delete_after_new_pages_already_published(tmp_path):
    retired, kept = argument("Retiré"), argument("Conservé")
    p, config, path, adapter = plan(tmp_path, old_pages=[("fr","A1","Retiré",retired),("fr","A2","Conservé",kept)], new_pages=[("fr","A2","Conservé",kept)], remote_pages={("fr","Retiré"):(10,retired),("fr","Conservé"):(20,kept)})
    receipt = module.PlanExecutor(config, adapter, path).execute(p, p["plan_sha256"], only_delete=True)
    assert receipt["counts"]["deleted"] == 1
    assert ("fr","Retiré") not in adapter.pages


def test_signed_read_only_remote_inventory_is_last_resort(tmp_path):
    text = argument("Inventorié")
    config, path = make_fixture(tmp_path, old_pages=[], new_pages=[("fr", "A1", "Titre", text)])
    state_path = tmp_path / ".state/published/demo/fr/latest.json"
    state_path.unlink()
    inventory = {
        "inventory_version": "1.0",
        "inventory_mode": "explicit_debate_pages_read_only",
        "debate_id": "demo",
        "language": "fr",
        "generated_at": "2026-07-31T20:00:00Z",
        "pages": [{
            "page_id": "A1",
            "page_type": "argument",
            "canonical_title": "Titre",
            "content_sha256": module.sha_text(text),
            "revision_id": 10,
            "status": "published",
            "content": text,
        }],
    }
    inventory["inventory_sha256"] = module.sha_object(inventory)
    inv_path = tmp_path / ".state/inventories/demo/fr.json"
    inv_path.parent.mkdir(parents=True)
    inv_path.write_text(json.dumps(inventory), encoding="utf-8")
    adapter = FakeAdapter({("fr", "Titre"): (10, text)})
    planner = module.RemoteUpdatePlanner(config, adapter, path)
    plan_data = planner.build_plan()
    assert plan_data["state_source"]["kind"] == "remote_inventory"
    assert plan_data["counts"]["skip"] == 1


def test_default_update_summary_is_concise(tmp_path):
    config, config_path = make_fixture(tmp_path, old_pages=[], new_pages=[])
    executor = module.PlanExecutor(config, FakeAdapter(), config_path)
    assert executor._summary("fr", "update", {"corpus_version":"manifest-deadbeef"}) == "Corrections"
    assert executor._summary("en", "update", {"corpus_version":"manifest-deadbeef"}) == "Corrections"


def test_16_manual_review_plan_cannot_be_executed_or_rewrite_state(tmp_path):
    old, human, new = argument("Ancien"), argument("Modification humaine"), argument("Nouveau")
    p, config, path, adapter = plan(
        tmp_path,
        old_pages=[("fr", "A1", "Titre", old)],
        new_pages=[("fr", "A1", "Titre", new)],
        remote_pages={("fr", "Titre"): (11, human)},
    )
    assert p["counts"]["manual_review"] == 1
    executor = module.PlanExecutor(config, adapter, path)
    try:
        executor.execute(p, p["plan_sha256"])
    except module.PlanConflict as exc:
        assert "révision manuelle" in str(exc)
    else:
        raise AssertionError("un plan manual_review a été exécuté")
    assert not (tmp_path / ".state" / "receipts").exists()
    latest = tmp_path / ".state" / "published" / "demo" / "fr" / "latest.json"
    state = json.loads(latest.read_text(encoding="utf-8"))
    assert state["pages"][0]["content_sha256"] == module.sha_text(old)


def test_17_all_skip_plan_cannot_create_false_success_receipt(tmp_path):
    text = argument("Même")
    p, config, path, adapter = plan(
        tmp_path,
        old_pages=[("fr", "A1", "Titre", text)],
        new_pages=[("fr", "A1", "Titre", text)],
        remote_pages={("fr", "Titre"): (10, text)},
    )
    executor = module.PlanExecutor(config, adapter, path)
    try:
        executor.execute(p, p["plan_sha256"])
    except module.PlanConflict as exc:
        assert "aucune opération exécutable" in str(exc)
    else:
        raise AssertionError("un plan entièrement skip a créé un faux succès")
    assert not (tmp_path / ".state" / "receipts").exists()


def test_18_no_changes_attestation_refreshes_state_for_next_update(tmp_path):
    old = argument("Ancien état")
    current = argument("Déjà présent à distance")
    p, config, path, adapter = plan(
        tmp_path,
        old_pages=[("fr", "A1", "Titre", old)],
        new_pages=[("fr", "A1", "Titre", current)],
        remote_pages={("fr", "Titre"): (20, current)},
    )
    assert p["counts"]["skip"] == 1
    receipt = module.PlanExecutor(config, adapter, path).attest_no_changes(p, p["plan_sha256"])
    assert receipt["status"] == "no_changes"
    assert receipt["counts"] == {"verified_unchanged": 1}
    state_path = tmp_path / ".state" / "published" / "demo" / "fr" / "latest.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["pages"][0]["content_sha256"] == module.sha_text(current)
    assert state["pages"][0]["revision_id"] == 20

    proposed = argument("Modification suivante")
    (tmp_path / "corpus" / "demo" / "output" / "fr" / "A1.wiki").write_text(proposed, encoding="utf-8")
    next_plan = module.RemoteUpdatePlanner(config, adapter, path).build_plan()
    assert next_plan["counts"]["update"] == 1
    assert next_plan["counts"]["manual_review"] == 0


def test_19_no_changes_attestation_detects_remote_change_after_plan(tmp_path):
    text = argument("Même contenu")
    p, config, path, adapter = plan(
        tmp_path,
        old_pages=[("fr", "A1", "Titre", text)],
        new_pages=[("fr", "A1", "Titre", text)],
        remote_pages={("fr", "Titre"): (10, text)},
    )
    adapter.pages[("fr", "Titre")] = (11, argument("Changement concurrent"))
    try:
        module.PlanExecutor(config, adapter, path).attest_no_changes(p, p["plan_sha256"])
    except module.PlanConflict as exc:
        assert "modifié depuis le plan" in str(exc)
    else:
        raise AssertionError("une attestation obsolète a été acceptée")
    assert not (tmp_path / ".state" / "receipts").exists()


def test_20_no_delete_preserves_pending_pages_for_later_only_delete(tmp_path):
    retired = argument("Retiré")
    old_kept = argument("Ancienne version")
    new_kept = argument("Nouvelle version")
    p, config, path, adapter = plan(
        tmp_path,
        old_pages=[
            ("fr", "A1", "Retiré", retired),
            ("fr", "A2", "Conservé", old_kept),
        ],
        new_pages=[("fr", "A2", "Conservé", new_kept)],
        remote_pages={
            ("fr", "Retiré"): (10, retired),
            ("fr", "Conservé"): (20, old_kept),
        },
    )
    receipt = module.PlanExecutor(config, adapter, path).execute(p, p["plan_sha256"], no_delete=True)
    assert receipt["counts"]["updated"] == 1
    assert ("fr", "Retiré") in adapter.pages
    state_path = tmp_path / ".state" / "published" / "demo" / "fr" / "latest.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    statuses = {row["page_id"]: row["status"] for row in state["pages"]}
    assert statuses == {"A1": "pending_delete", "A2": "published"}

    delete_plan = module.RemoteUpdatePlanner(config, adapter, path).build_plan()
    assert delete_plan["counts"]["delete"] == 1
    assert delete_plan["counts"]["manual_review"] == 0
    delete_receipt = module.PlanExecutor(config, adapter, path).execute(
        delete_plan,
        delete_plan["plan_sha256"],
        only_delete=True,
    )
    assert delete_receipt["counts"]["deleted"] == 1
    assert ("fr", "Retiré") not in adapter.pages
    final_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert [row["page_id"] for row in final_state["pages"]] == ["A2"]


def test_move_is_blocked_if_protected_warning_would_change(tmp_path):
    old = argument('Ancien')
    new = argument('Nouveau').replace(MARKER, '')
    p, *_ = plan(
        tmp_path,
        old_pages=[('fr','A1','Ancien titre',old)],
        new_pages=[('fr','A1','Nouveau titre',new)],
        remote_pages={('fr','Ancien titre'):(10,old)},
    )
    assert p['counts']['move'] == 0
    assert p['counts']['blocked'] == 1
    assert 'protégé' in p['operations']['blocked'][0]['justification']


def test_deferred_translation_blocks_english_remote_update_scope(tmp_path):
    config, path = make_fixture(
        tmp_path,
        languages=("en",),
        old_pages=[],
        new_pages=[("en", "A1", "English title", argument("English"))],
    )
    manifest_path = tmp_path / "corpus" / "demo" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["normative_versions"] = {"consolidated_norm": "1.2.34"}
    manifest["translation_status"] = {"en": "deferred"}
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    try:
        module.RemoteUpdatePlanner(config, FakeAdapter(), path)
    except module.UpdateError as exc:
        assert "deferred" in str(exc)
    else:
        raise AssertionError("reprise anglaise acceptée pendant la traduction différée")
