from pathlib import Path
import importlib.util
import sys

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod; spec.loader.exec_module(mod); return mod

def test_corpus_init_preserves_bounded_or_unbounded_depth_policy():
    text=(ROOT/'scripts/wikidebia_corpus_init.py').read_text(encoding='utf-8')
    assert '"limit_policy": "unbounded"' in text
    assert '"limit_policy": "bounded"' in text
    assert '"frontier_node_ids"' in text
    assert 'Profondeur exceptionnelle élevée' not in text


def test_corpus_init_records_depth_frontiers_from_limited_snapshot():
    module = load("wikidebia_corpus_init_depth", ROOT / "scripts/wikidebia_corpus_init.py")
    graph = {
        "metadata": {
            "limite_profondeur": 3,
            "relations_ignorees_limite_profondeur": 7,
        },
        "frontières_profondeur": {"Argument frontière": 7},
    }
    policy = module._depth_policy(graph, {"Argument frontière": "A0004"}, 4)
    assert policy == {
        "limit_policy": "bounded",
        "maximum_observed": 4,
        "maximum_edge_depth": 3,
        "frontier_node_ids": ["A0004"],
        "relations_omitted_at_frontier": 7,
    }


def test_corpus_init_keeps_unbounded_policy_without_requested_limit():
    module = load("wikidebia_corpus_init_unbounded", ROOT / "scripts/wikidebia_corpus_init.py")
    assert module._depth_policy({"metadata": {}}, {}, 5) == {
        "limit_policy": "unbounded",
        "maximum_observed": 5,
    }

def test_editorial_review_requires_keyword_relevance_order():
    text=(ROOT/'scripts/wikidebia_editorial_review.py').read_text(encoding='utf-8')
    assert 'keywords_ordered_by_relevance' in text
    assert 'keyword_order_rationale' in text

def test_translation_preserves_keyword_relevance_order():
    text=(ROOT/'scripts/wikidebia_translation_review.py').read_text(encoding='utf-8')
    assert 'keywords_order_preserved_by_relevance' in text
