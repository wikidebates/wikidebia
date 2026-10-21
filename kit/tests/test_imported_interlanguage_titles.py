import json

import pytest

from test_wikidebia_remote_update import FakeAdapter, argument, make_fixture, module


TITLES = [
    "La prohibition du cannabis expose les usagers à l’univers des dealers et à des drogues plus dures",
    "La prohibition du cannabis entraîne le développement d'une économie parallèle très lucrative avec ses conséquences : corruption, blanchiment d’argent, recrutement de jeunes, violence, insécurité, trafic d'armes",
    "Le cannabis potentialise les effets de l’alcool et du tabac",
]


def fixture(tmp_path, *, title=TITLES[0], drift=None):
    remote = argument("Texte et citation historiques conservés")
    normalized = title.replace("’", "'")
    config, path = make_fixture(
        tmp_path,
        old_pages=[("fr", "A1", normalized, remote)],
        new_pages=[("fr", "A1", normalized, argument("Texte local à ne pas publier"))],
    )
    corpus = tmp_path / "corpus/demo"
    english = corpus / "output/en/A1.wiki"
    english.parent.mkdir(parents=True)
    english.write_text("{{Argument\n|summary=English\n}}\n", encoding="utf-8")
    manifest = json.loads((corpus / "manifest.json").read_text())
    manifest["translation_status"] = {"en": "ready"}
    manifest["pages"].append({
        "language": "en", "page_id": "A1", "page_type": "argument",
        "canonical_title": "English title", "file_path": "output/en/A1.wiki",
        "sha256": module.sha_file(english),
    })
    (corpus / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    config["interlanguage_only"] = True
    path.write_text(json.dumps(config), encoding="utf-8")
    imported = corpus / "imports/fr/arguments/A1.wiki"
    imported.parent.mkdir(parents=True)
    imported.write_text(remote, encoding="utf-8")
    record = {
        "page_id": "A1", "kind": "argument", "canonical_title": title,
        "revision_id": 11, "import_path": "imports/fr/arguments/A1.wiki",
        "sha256": module.sha_file(imported),
    }
    data = corpus / "data"
    data.mkdir(exist_ok=True)
    if drift == "source":
        imported.write_text("Changed snapshot", encoding="utf-8")
    if drift == "title":
        record["canonical_title"] = "An unrelated page"
    if drift == "revision":
        record["revision_id"] = 0
    if drift != "missing_provenance":
        (data / "import_provenance.json").write_text(json.dumps({"pages": [record]}), encoding="utf-8")
    pages = {("fr", title): (12 if drift == "human_revision" else 11, remote)}
    if drift == "remote_content":
        pages[("fr", title)] = (11, remote + "Unrecorded change")
    return config, path, FakeAdapter(pages), remote


@pytest.mark.parametrize("title", TITLES)
def test_exact_imported_title_unblocks_only_a_pure_interlanguage_addition(tmp_path, title):
    config, path, adapter, original = fixture(tmp_path, title=title)
    plan = module.RemoteUpdatePlanner(config, adapter, path).build_plan()
    assert plan["counts"]["blocked"] == 0
    assert plan["counts"]["update"] == 1
    operation = plan["operations"]["update"][0]
    assert operation["title"] == title
    assert operation["interlanguage_title_resolution"]["source_title"] == title
    module.PlanExecutor(config, adapter, path).execute(plan, plan["plan_sha256"])
    final = adapter.pages[("fr", title)][1]
    expected, _ = module.add_french_interlanguage_to_remote(original, "argument", "English title")
    assert final == expected
    assert len(adapter.pages) == 1
    assert [event[0] for event in adapter.events].count("write") == 1
    assert not any(event[0] in {"move", "delete"} for event in adapter.events)
    state = json.loads((tmp_path / ".state/published/demo/fr/latest.json").read_text())
    assert state["pages"][0]["canonical_title"] == title
    resumed = module.RemoteUpdatePlanner(config, adapter, path).build_plan()
    assert resumed["counts"]["skip"] == 1
    assert resumed["counts"]["blocked"] == 0


@pytest.mark.parametrize("drift", ["source", "title", "revision", "missing_provenance", "human_revision", "remote_content"])
def test_unproven_import_identity_remains_blocked(tmp_path, drift):
    config, path, adapter, _ = fixture(tmp_path, drift=drift)
    plan = module.RemoteUpdatePlanner(config, adapter, path).build_plan()
    assert plan["counts"]["blocked"] == 1
    assert plan["counts"]["update"] == 0
    assert not any(event[0] == "write" for event in adapter.events)


def test_existing_manifest_title_is_never_replaced_by_a_fallback(tmp_path):
    config, path, adapter, original = fixture(tmp_path)
    normalized = TITLES[0].replace("’", "'")
    adapter.pages[("fr", normalized)] = (19, original)
    plan = module.RemoteUpdatePlanner(config, adapter, path).build_plan()
    operation = plan["operations"]["update"][0]
    assert operation["title"] == normalized
    assert "interlanguage_title_resolution" not in operation
