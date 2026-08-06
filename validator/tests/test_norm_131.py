from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_graph_validator_has_unbounded_policy_without_current_threshold_warning():
    text=(ROOT/'src/wikidebia_validator/graph.py').read_text(encoding='utf-8')
    assert 'if norm in {"1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37", "1.2.38", "1.2.39", "1.2.40", "1.2.41"}' in text
    assert 'policy.get("limit_policy") != "unbounded"' in text
    current=text.split('if norm in {"1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37", "1.2.38", "1.2.39", "1.2.40", "1.2.41"}:',1)[1].split('else:',1)[0]
    assert 'Profondeur exceptionnelle élevée' not in current

def test_active_norm_orders_keywords_by_relevance():
    text=(ROOT/'normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.41.md').read_text(encoding='utf-8')
    assert 'du plus directement pertinent au moins directement pertinent' in text
    assert 'L’ordre chronologique' in text


def test_current_norm_does_not_warn_on_high_depth(tmp_path):
    import json
    from wikidebia_validator.validator import validate_package
    from .helpers import create_graph_package, dump
    create_graph_package(tmp_path)
    manifest_path=tmp_path/'manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['normative_versions']['consolidated_norm']='1.2.32'
    dump(manifest_path,manifest)
    reg_path=tmp_path/'data/registre_debat.json'
    reg=json.loads(reg_path.read_text(encoding='utf-8'))
    # One node is enough to test a descriptive maximum without introducing a bad relation.
    reg['graph']['occurrences'][0]['depth']=9
    reg['graph']['depth_policy']={'limit_policy':'unbounded','maximum_observed':9}
    reg['graph']['derived_counts']['maximum_depth']=9
    reg['graph']['nodes'][0]['derived']['minimum_depth']=9
    reg['graph']['nodes'][0]['derived']['maximum_depth']=9
    dump(reg_path,reg)
    report=validate_package(tmp_path,scopes=['graph'])
    assert not any(f.level=='WARNING' and 'Profondeur exceptionnelle élevée' in f.message for f in report.findings)
