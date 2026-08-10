import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NORM = ROOT / 'normative_reference' / '01_normes'


def test_reconciliation_has_single_active_norm_and_noncolliding_requirements():
    active = sorted(p.name for p in NORM.glob('WIKIDEBIA_NORME_CONSOLIDEE_*.md'))
    assert active == ['WIKIDEBIA_NORME_CONSOLIDEE_1.2.68.md']
    data = json.loads((NORM / 'requirements_catalog_wikidebia.json').read_text(encoding='utf-8'))
    rows = data['requirements']
    ids = [row['id'] for row in rows]
    assert len(ids) == len(set(ids))
    by_id = {row['id']: row for row in rows}
    for req_id in ('PUB-045', 'PUB-046', 'PUB-047', 'TRN-009', 'TRN-019', 'RND-007', 'RND-009', 'ARCH-008'):
        assert req_id in by_id
    assert 'differential' in by_id['TRN-009']['statement'].lower()
    assert 'initialization' in by_id['TRN-019']['statement']
    assert 'complete citation' in by_id['RND-007']['statement'].lower()
    assert 'creation-date' in by_id['RND-009']['statement']


def test_reconciliation_preserves_both_branch_histories():
    history = NORM / 'history'
    assert (history / 'translation_branch' / 'WIKIDEBIA_NORME_CONSOLIDEE_1.2.61__translation_branch.md').is_file()
    assert (history / 'parallel_publication_branch' / 'WIKIDEBIA_NORME_CONSOLIDEE_1.2.60__github_8b46816.md').is_file()
    active = (NORM / 'WIKIDEBIA_NORME_CONSOLIDEE_1.2.68.md').read_text(encoding='utf-8')
    assert 'Translation of the French page: [[:fr:X|X]]' in active
    assert 'AI-translated quote' in active
    assert '`nom-consacré=` / `established-name=`' in active or 'nom-consacré' in active and 'established-name' in active
    assert 'ne transporte jamais `|initialisation=`/`|initialization=`' in active


def test_current_wikicode_contract_combines_translation_and_publication_rules():
    from wikidebia_validator import wikicode
    assert wikicode.TOP['en', 'argument']['order'][:3] == ['initialization', 'established-name', 'name']
    assert 'initialization' in wikicode.TOP['en', 'argument']['forbidden_generated']
    assert 'established-name' in wikicode.PROTECTED_PAGE_PARAMETERS['en', 'argument']
    source = (ROOT / 'src' / 'wikidebia_validator' / 'wikicode.py').read_text(encoding='utf-8')
    assert 'AI-translated quote' in source
