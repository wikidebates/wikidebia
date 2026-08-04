import importlib.util
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "wikidebia_graph_extract.py"
spec = importlib.util.spec_from_file_location("graphmod", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class FakeClient:
    def __init__(self, pages, aliases=None):
        self.pages = pages
        self.aliases = aliases or {}

    def fetch(self, title):
        canonical = self.aliases.get(title, title)
        if canonical not in self.pages:
            raise mod.PageMissingError(title)
        return mod.PageRecord(
            requested_title=title,
            canonical_title=canonical,
            text=self.pages[canonical],
            url=f"https://example.test/wiki/{canonical}",
            revision_id=1,
        )


class ParserTests(unittest.TestCase):
    def test_nested_debate_templates(self):
        text = """{{Débat
|arguments-pour={{Argument pour|page=A|titre-affiché=A prouve P}}{{Argument pour|page=B}}
|arguments-contre={{Argument contre|page=C}}
}}"""
        parsed = mod.parse_debate_wikitext(text)
        self.assertEqual([x.page for x in parsed.pro], ["A", "B"])
        self.assertEqual([x.page for x in parsed.con], ["C"])
        self.assertEqual(parsed.pro[0].displayed_title, "A prouve P")

    def test_frontier_discards_relations(self):
        text = """{{Argument
|débat-détaillé=[[Débat sous-jacent]]
|justifications={{Justification|page=X}}
|objections={{Objection|page=Y}}
}}"""
        parsed = mod.parse_argument_wikitext(text)
        self.assertEqual(parsed.detailed_debate, "Débat sous-jacent")
        self.assertEqual(parsed.justifications, [])
        self.assertEqual(parsed.objections, [])
        self.assertEqual(parsed.ignored_relations_at_frontier, 2)


class CrawlTests(unittest.TestCase):
    def test_recursive_graph_reuse_and_redirect(self):
        pages = {
            "Débat test": """{{Débat
|arguments-pour={{Argument pour|page=A}}
|arguments-contre={{Argument contre|page=B}}
}}""",
            "A": """{{Argument
|justifications={{Justification|page=Alias C}}
|objections={{Objection|page=B}}
}}""",
            "B": "{{Argument|justifications=|objections=}}",
            "C": """{{Argument
|débat détaillé=Débat C
|justifications={{Justification|page=X}}
|objections=
}}""",
        }
        client = FakeClient(pages, aliases={"Alias C": "C"})
        result = mod.crawl_graph(client, debate_title="Débat test", progress_every=0)
        graph = mod.analyze_graph(result)
        meta = graph["metadata"]
        self.assertEqual(meta["pages_arguments_uniques"], 3)
        self.assertEqual(meta["relations_uniques"], 2)
        self.assertEqual(meta["pages_uniques_par_niveau_minimal"], {1: 2, 2: 1})
        self.assertEqual(meta["occurrences_par_niveau"], {1: 2, 2: 2})
        self.assertEqual(meta["frontières_débat_détaillé"], {"C": "Débat C"})
        b = next(row for row in graph["noeuds"] if row["titre"] == "B")
        self.assertEqual(b["occurrences_totales"], 2)

    def test_snapshot_and_package_are_complete(self):
        pages = {
            "Débat test": "{{Débat|arguments-pour={{Argument pour|page=A}}|arguments-contre=}}",
            "A": "{{Argument|justifications={{Justification|page=B}}|objections=}}",
            "B": "{{Argument|justifications=|objections=}}",
        }
        result = mod.crawl_graph(FakeClient(pages), debate_title="Débat test", progress_every=0)
        graph = mod.analyze_graph(result)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            paths = mod.write_outputs(
                graph, result, output_dir=output, slug="debat_test", extraction_date="2026-08-03"
            )
            snapshot = json.loads(paths["snapshot_manifest"].read_text(encoding="utf-8"))
            self.assertEqual(snapshot["counts"], {"debate_pages": 1, "argument_pages": 2, "total_pages": 3})
            self.assertEqual(len(snapshot["arguments"]), 2)
            package = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            self.assertEqual(package["audit_status"], "passed")
            self.assertGreater(package["declared_file_count"], 6)
            with zipfile.ZipFile(paths["zip"]) as archive:
                names = set(archive.namelist())
            self.assertIn("snapshot/snapshot_manifest.json", names)
            self.assertIn("snapshot/pages/debate.wiki", names)

    def test_cache_is_reusable(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = mod.JsonPageCache(Path(directory))
            record = mod.PageRecord(
                requested_title="Alias", canonical_title="A", text="texte", revision_id=7
            )
            cache.put(record)
            self.assertEqual(cache.get("Alias").canonical_title, "A")
            self.assertEqual(cache.get("A").revision_id, 7)

    def test_cycle_is_reported(self):
        pages = {
            "Débat test": "{{Débat|arguments-pour={{Argument pour|page=A}}|arguments-contre=}}",
            "A": "{{Argument|justifications={{Justification|page=B}}|objections=}}",
            "B": "{{Argument|justifications={{Justification|page=A}}|objections=}}",
        }
        graph = mod.analyze_graph(
            mod.crawl_graph(FakeClient(pages), debate_title="Débat test", progress_every=0)
        )
        self.assertFalse(graph["metadata"]["graphe_sans_cycle"])
        self.assertTrue(graph["metadata"]["nœuds_dans_cycles"])


if __name__ == "__main__":
    unittest.main()


class SafetyTests(unittest.TestCase):
    def test_extractor_contains_no_pywikibot_write_call(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = ("page.save(", "page.put(", "page.delete(", "page.move(", "editpage(", "submit(")
        self.assertFalse([token for token in forbidden if token in source])

    def test_anonymous_read_does_not_require_user_config(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = mod.JsonPageCache(Path(directory) / "cache")
            client = mod.PywikibotPageClient(
                family="wikidebates",
                lang="fr",
                family_file=None,
                pywikibot_dir=Path(directory) / "private",
                cache=cache,
                login=False,
            )
            self.assertFalse(client.login)
