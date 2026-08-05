from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def test_corpus_init_uses_unbounded_depth_policy():
    text=(ROOT/'scripts/wikidebia_corpus_init.py').read_text(encoding='utf-8')
    assert '"limit_policy": "unbounded"' in text
    assert 'Profondeur exceptionnelle élevée' not in text

def test_editorial_review_requires_keyword_relevance_order():
    text=(ROOT/'scripts/wikidebia_editorial_review.py').read_text(encoding='utf-8')
    assert 'keywords_ordered_by_relevance' in text
    assert 'keyword_order_rationale' in text

def test_translation_preserves_keyword_relevance_order():
    text=(ROOT/'scripts/wikidebia_translation_review.py').read_text(encoding='utf-8')
    assert 'keywords_order_preserved_by_relevance' in text
