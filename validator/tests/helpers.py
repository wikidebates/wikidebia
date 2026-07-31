from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from wikidebia_validator.graph import compute_derived, structural_sha256

NOW = "2026-07-23T18:00:00+02:00"
DATE = "2026-07-23"
ZERO = "0" * 64


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wiki_record():
    return {"check_status": "unchecked", "decision": None, "remote_revision_id": None, "remote_sha256": None, "published_at": None, "checked_at": None, "remote_title": None}


def generation(status="pending", batch=None):
    if status == "pending":
        return {"status": status, "assigned_batch_id": batch, "creation_date": None, "generated_at": None, "validated_at": None}
    return {"status": status, "assigned_batch_id": batch, "creation_date": DATE, "generated_at": NOW, "validated_at": NOW if status == "validated" else None}


def file_record(path, status="absent", hash_value=None):
    return {"path": path, "sha256": hash_value, "status": status}


def fr_interlanguage(status="pending", target=None):
    return {"status": status, "target_language": "en", "target_title": target, "inserted_at": None, "verified_at": None}


def en_interlanguage():
    return {"status": "not_applicable"}


def arg_page_record(lang, node_id, status="pending", batch=None, hash_value=None):
    path = f"output/{lang}/arguments/{node_id}.wiki"
    return {
        "generation": generation(status, batch),
        "file": file_record(path, "validated" if status == "validated" else "absent", hash_value),
        "wiki": wiki_record(),
        "interlanguage": fr_interlanguage() if lang == "fr" else en_interlanguage(),
    }


def debate_page_record(lang, title, status="pending", hash_value=None):
    path = f"output/{lang}/debate/debate.wiki"
    return {
        "canonical_title": title,
        "title_status": "locked" if title else "unassigned",
        "generation": generation(status),
        "file": file_record(path, "validated" if status == "validated" else "absent", hash_value),
        "wiki": wiki_record(),
        "interlanguage": fr_interlanguage() if lang == "fr" else en_interlanguage(),
    }


def make_registry(full_fr=False):
    nodes = []
    titles = [
        ("A0001", "La mesure X produirait un bénéfice collectif", "Un bénéfice collectif", "pro"),
        ("A0002", "La mesure X porterait une atteinte disproportionnée aux libertés", "Une atteinte disproportionnée", "con"),
    ]
    occurrences = []
    for idx, (nid, title_fr, displayed_fr, branch) in enumerate(titles, 1):
        node = {
            "id": nid,
            "status": "active",
            "fr": {"canonical_title": title_fr, "displayed_title": displayed_fr, "title_status": "locked", "rubriques": ["Société"], "keywords": ["mesure X"]},
            "en": {"canonical_title": None, "displayed_title": None, "title_status": "unassigned", "sections": [], "keywords": []},
            "pages": {
                "fr": arg_page_record("fr", nid, "pending"),
                "en": arg_page_record("en", nid, "pending"),
            },
            "sources": {"fr": {"bibliography": [], "webliography": [], "videography": []}, "en": {"bibliography": [], "webliography": [], "videography": []}},
        }
        nodes.append(node)
        occurrences.append({"id": f"O{idx:05d}", "node_id": nid, "parent_occurrence_id": None, "edge_id": None, "branch": branch, "depth": 1, "order": 1, "occurrence_role": "primary", "render_children": False})
    registry = {
        "schema": {"registry_version": "1.0", "graph_version": "1.0", "mediawiki_structure_version": "1.0", "render_profile_version": "1.0", "validator_version": "0.2.1"},
        "debate": {
            "id": "exemple",
            "scope": {"proposition_fr": "Faut-il adopter la mesure X ?", "scope_summary_fr": "Débat pilote.", "jurisdiction": None, "timeframe": None, "included_topics": [], "excluded_topics": [], "residual_ambiguities": []},
            "labels": {"fr": {"pro": "Arguments pour l'adoption", "con": "Arguments contre l'adoption"}, "en": {"pro": None, "con": None}},
            "pages": {
                "fr": debate_page_record("fr", "Faut-il adopter la mesure X ?", "pending"),
                "en": debate_page_record("en", None, "pending"),
            },
        },
        "graph": {
            "lifecycle": {"status": "locked", "validated_at": NOW, "locked_at": NOW, "locked_by_stage": "graph_finalization", "structural_sha256": None},
            "depth_policy": {"normal_target": 3, "declared_maximum": 3, "exception_reason": None, "maximum_observed": 1},
            "nodes": nodes,
            "edges": [],
            "occurrences": occurrences,
            "derived_counts": {},
        },
        "batches": [], "validations": [], "migrations": [],
    }
    counts, per_node = compute_derived(registry)
    registry["graph"]["derived_counts"] = counts
    for node in nodes:
        node["derived"] = per_node[node["id"]]
    registry["graph"]["lifecycle"]["structural_sha256"] = structural_sha256(registry)
    return registry


def scope_doc():
    return {
        "scope_schema_version": "1.0", "debate_id": "exemple", "canonical_title_fr": "Faut-il adopter la mesure X ?",
        "proposition_fr": "Faut-il adopter la mesure X ?", "scope_summary_fr": "Débat pilote.", "jurisdiction": None,
        "timeframe": None, "included_topics": [], "excluded_topics": [], "residual_ambiguities": [], "related_debates": [],
        "editorial_constraints": [], "source_documents": [],
    }


def graph_projection(registry):
    g = registry["graph"]
    return {
        "graph_schema_version": "1.0",
        "debate": {"id": "exemple", "title_fr": "Faut-il adopter la mesure X ?", "labels": copy.deepcopy(registry["debate"]["labels"])},
        "lifecycle": copy.deepcopy(g["lifecycle"]), "depth_policy": copy.deepcopy(g["depth_policy"]),
        "nodes": copy.deepcopy(g["nodes"]), "edges": copy.deepcopy(g["edges"]), "occurrences": copy.deepcopy(g["occurrences"]),
        "derived_counts": copy.deepcopy(g["derived_counts"]),
    }


def validation(scope):
    return {"id": f"V20260723-{len(scope):03d}", "scope": scope, "language": None if scope in {"graph", "bilingual", "release"} else ("fr" if scope.startswith("fr") else "en"), "validator_version": "0.2.1", "executed_at": NOW, "input_sha256": ZERO, "result": "passed", "blocking_errors": 0, "warnings": 0, "report_path": f"reports/{scope}.txt"}


def base_manifest(status="graph_locked"):
    return {
        "package_schema_version": "1.0", "debate_id": "exemple", "short_code": "EX", "global_status": status,
        "created_at": NOW, "updated_at": NOW,
        "normative_versions": {"mediawiki_structure": "1.0", "render_profile": "1.0", "registry": "1.0", "graph": "1.0", "workflow": "1.0", "validator": "0.2.1"},
        "core_files": {"scope": "scope.json", "registry": "data/registre_debat.json", "graph_json": "graph/graphe_argumentatif.json", "graph_markdown": "graph/graphe_argumentatif.md", "sources": "data/sources.json"},
        "pages": [], "batches": [], "works": [], "validations": [validation("graph")],
        "release": {"release_manifest_path": None, "release_zip_path": None, "released_at": None, "archived_at": None, "release_receipt_path": None},
    }


def create_graph_package(root: Path) -> Path:
    registry = make_registry()
    manifest = base_manifest()
    dump(root / "manifest.json", manifest)
    dump(root / "scope.json", scope_doc())
    dump(root / "data/registre_debat.json", registry)
    dump(root / "data/sources.json", {"source_registry_version": "1.0", "debate_id": "exemple", "sources": []})
    dump(root / "graph/graphe_argumentatif.json", graph_projection(registry))
    text(root / "graph/graphe_argumentatif.md", "Faut-il adopter la mesure X ?")
    text(root / "graph/validation_report.txt", "VALIDATION GLOBALE : RÉUSSIE")
    text(root / "reports/graph.txt", "passed")
    return root


def page_manifest(page_id, page_type, lang, title, file_path, hash_value, batch_id=None):
    return {
        "page_manifest_version": "1.0", "debate_id": "exemple", "page_id": page_id, "page_type": page_type,
        "language": lang, "canonical_title": title, "file_path": file_path, "sha256": hash_value, "creation_date": DATE,
        "batch_id": batch_id, "status": "validated", "structure_version": "1.0", "render_profile_version": "1.0",
        "validation": {"status": "passed", "report_path": f"reports/{page_id}_{lang}.txt", "validated_at": NOW},
        "wiki": wiki_record(),
    }


def create_fr_package(root: Path) -> Path:
    registry = make_registry()
    debate_wiki = """{{Débat
|sujet=Mesure X
|sujet-complet=l'adoption de la mesure X
|avancement=Débat construit
|avertissements-débat=Débat généré par IA
|introduction={{Sous-partie
|titre=Définition
|contenu=La mesure X est une mesure pilote.
}}
|arguments-pour={{Argument pour
|page=La mesure X produirait un bénéfice collectif
|titre-affiché=Un bénéfice collectif
}}
|arguments-contre={{Argument contre
|page=La mesure X porterait une atteinte disproportionnée aux libertés
|titre-affiché=Une atteinte disproportionnée
}}
|rubriques=Société
|mots-clés=mesure X
|date-création=2026-07-23
}}"""
    arg1 = """{{Argument
|avertissements-argument=Argument généré par IA
|résumé=La mesure X mutualiserait certains bénéfices et réduirait des coûts collectifs.
|rubriques=Société
|mots-clés=mesure X
|date-création=2026-07-23
}}"""
    arg2 = """{{Argument
|avertissements-argument=Argument généré par IA
|résumé=La mesure X limiterait certaines libertés au-delà de ce qui serait nécessaire.
|rubriques=Société
|mots-clés=mesure X
|date-création=2026-07-23
}}"""
    text(root / "output/fr/debate/debate.wiki", debate_wiki)
    text(root / "output/fr/arguments/A0001.wiki", arg1)
    text(root / "output/fr/arguments/A0002.wiki", arg2)
    pages = [
        page_manifest("exemple", "debate", "fr", "Faut-il adopter la mesure X ?", "output/fr/debate/debate.wiki", sha(root / "output/fr/debate/debate.wiki")),
        page_manifest("A0001", "argument", "fr", "La mesure X produirait un bénéfice collectif", "output/fr/arguments/A0001.wiki", sha(root / "output/fr/arguments/A0001.wiki"), "FR-A-001"),
        page_manifest("A0002", "argument", "fr", "La mesure X porterait une atteinte disproportionnée aux libertés", "output/fr/arguments/A0002.wiki", sha(root / "output/fr/arguments/A0002.wiki"), "FR-A-001"),
    ]
    for node in registry["graph"]["nodes"]:
        p = next(x for x in pages if x["page_id"] == node["id"])
        node["pages"]["fr"] = arg_page_record("fr", node["id"], "validated", "FR-A-001", p["sha256"])
    dpage = pages[0]
    registry["debate"]["pages"]["fr"] = debate_page_record("fr", "Faut-il adopter la mesure X ?", "validated", dpage["sha256"])
    aggregate = "===== PAGE : La mesure X produirait un bénéfice collectif =====\n" + arg1 + "\n\n===== PAGE : La mesure X porterait une atteinte disproportionnée aux libertés =====\n" + arg2 + "\n"
    text(root / "output/fr/aggregates/arguments_batch_001.wiki", aggregate)
    batch = {
        "batch_schema_version": "1.0", "id": "FR-A-001", "debate_id": "exemple", "language": "fr", "page_type": "argument", "strategy": "subtree",
        "root_node_ids": ["A0001", "A0002"], "node_ids": ["A0001", "A0002"], "dependency_node_ids": [], "status": "validated",
        "inputs": {"registry_sha256": ZERO, "structural_sha256": registry["graph"]["lifecycle"]["structural_sha256"], "render_profile_version": "1.0", "handoff_path": "handoff/FR-A-001_input.json"},
        "outputs": {"individual_directory": "output/fr/arguments", "aggregate_path": "output/fr/aggregates/arguments_batch_001.wiki", "aggregate_sha256": sha(root / "output/fr/aggregates/arguments_batch_001.wiki"), "report_path": "reports/fr_batch_001.txt"},
        "work": {"work_id": "W03.FR.001", "conversation_name": "[EX] 03.FR.001 — Arguments français — lot pilote", "started_at": NOW, "completed_at": NOW},
    }
    registry["batches"] = [copy.deepcopy(batch)]
    manifest = base_manifest("fr_validated")
    manifest["pages"] = pages
    manifest["batches"] = [copy.deepcopy(batch)]
    manifest["validations"] += [validation("fr_debate"), validation("fr_global")]
    dump(root / "manifest.json", manifest)
    dump(root / "scope.json", scope_doc())
    dump(root / "data/registre_debat.json", registry)
    dump(root / "data/sources.json", {"source_registry_version": "1.0", "debate_id": "exemple", "sources": []})
    dump(root / "data/lots_fr.json", {"batch_collection_version": "1.0", "debate_id": "exemple", "language": "fr", "batches": [batch]})
    dump(root / "graph/graphe_argumentatif.json", graph_projection(registry))
    text(root / "graph/graphe_argumentatif.md", "Faut-il adopter la mesure X ?")
    for name in ["graph", "fr_debate", "fr_global", "exemple_fr", "A0001_fr", "A0002_fr", "fr_batch_001"]:
        text(root / f"reports/{name}.txt", "passed")
    return root
