from pathlib import Path
import importlib.util
import sys

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
sys.path.insert(0,str(SCRIPTS))

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

def test_workspace_flags_uppercase_keywords_for_review():
    mod=load('workspace132',SCRIPTS/'wikidebia_editorial_workspace.py')
    issues=mod.keyword_diagnostics(['Revenu','justice sociale'],False,'argument')
    assert any(row.get('code')=='KEYWORDS_CAPITALIZATION_REVIEW' for row in issues)

def test_capitalization_helper_distinguishes_common_and_proper_terms():
    mod=load('workspace132b',SCRIPTS/'wikidebia_editorial_workspace.py')
    assert mod.keyword_capitalization_issues('revenu','noun')==[]
    assert mod.keyword_capitalization_issues('Revenu','noun')==['common_keyword_initial_uppercase']
    assert mod.keyword_capitalization_issues('Dieu','proper_name')==[]
    assert mod.keyword_capitalization_issues('ONU','acronym')==[]

def test_active_norm_documents_keyword_capitalization():
    # The exact normative source is packaged separately; kit enforcement is covered above.
    text=(SCRIPTS/'wikidebia_editorial_review.py').read_text(encoding='utf-8')
    assert 'capitalization_policy' in text
    assert 'capitalization_rationale' in text
