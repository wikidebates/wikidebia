from pathlib import Path
import collections, hashlib, json, sys
import mwparserfromhell as mw
O=Path(__file__).parent;W=O/'working-selected'
R=Path('/workspace/work/cannabis-translation-verification-20261021/relecture-approfondie/working')
P=Path('/workspace/work/cannabis-interquotation-code');N=P/'.state/editorial-workspaces/cannabis/EN-CANNABIS-20261021'
sys.path.insert(0,str(P/'kit/scripts'))
from wikidebia_render import _source_template
from wikidebia_translation_review import _validate_sources
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(n,c):
    checks.append(dict(check=n,passed=bool(c)));assert c,n
rows=load(W/'data/translation_pages.json');selected=load(O/'sources_en_selected.json')
sources,by_id=_validate_sources(selected,'cannabis',set())
reviews={r['delivery_id']:r for r in load(O/'page-documentary-selection-final.json')['rows']}
for r in rows:
    pid=r['id'];a=mw.parse((R/r['target_relative_path']).read_text());b=mw.parse((W/r['target_relative_path']).read_text())
    ta=next(t for t in a.filter_templates() if str(t.name).strip() in {'Argument','Debate'})
    tb=next(t for t in b.filter_templates() if str(t.name).strip() in {'Argument','Debate'})
    def non_doc(t):return [(str(p.name).strip(),str(p.value)) for p in t.params if str(p.name).strip() not in {'bibliography','webliography','videography'}]
    check(pid+'_all_non_documentary_fields_unchanged',non_doc(ta)==non_doc(tb))
    check(pid+'_recorded_target_hash',sha(W/r['target_relative_path'])==r['target_sha256'])
    doc_templates=[str(t).strip() for t in b.filter_templates() if str(t.name).strip() in {'Web reference','Bibliographical reference'}]
    # Inline historiques éventuellement présents dans les résumés sont protégés ;
    # comparer le contenu des trois champs documentaires seulement.
    actual=[str(t).strip() for bucket in ['bibliography','webliography','videography'] if tb.has(bucket) for t in mw.parse(str(tb.get(bucket).value)).filter_templates() if str(t.name).strip() in {'Web reference','Bibliographical reference'}]
    expected=[_source_template(by_id[sid],lang='en').strip() for sid in reviews[pid]['selected_source_ids']]
    check(pid+'_rendered_references_exact_selected_registry',collections.Counter(actual)==collections.Counter(expected))
    for sid in reviews[pid]['selected_source_ids']:
        use=next(u for u in by_id[sid]['usage'] if u['page_id']==reviews[pid]['native_id'])
        check(pid+'_'+sid+'_actual_argument_role',pid=='debate' or use['role']=='supports_summary' and use['argument_development_verified'] is True)
    check(pid+'_not_declared_ready',r['publication_ready'] is False)
for name in ['translation_texts.json','translation_quotes.json','translation_editorial_notes.json','relations_bilingual.json','labels_bilingual.json','vocabulary_bilingual.json']:
    check(name+'_unchanged_from_full_textual_review',sha(W/'data'/name)==sha(R/'data'/name))
prov=load(N/'reviewed-copy/data/import_provenance.json')['pages']
for r in rows:
    match=[p for p in prov if p['revision_id']==r['source_revision_id'] and p['sha256']==r['source_sha256']]
    check(r['id']+'_native_source_revision_hash_identity',len(match)==1)
check('149_native_quotes_2_native_passages',load(O/'native-citation-validation.json')['quotes']==149 and load(O/'native-citation-validation.json')['passages']==2)
check('1794_integrity_assertions_passed',load(O/'final-integrity-audit.json')['checks_passed']==1794)
check('no_structural_parameter_findings',not load(O/'parameters-after.json')['findings'])
check('no_false_native_translation_lock',not (N/'data/en_translation_lock.json').exists() and not (N/'content-reviewed-copy/data/fr_content_lock.json').exists())
result=dict(status='passed_integrity_and_documentary_selection_subset',checks_passed=len(checks),checks=checks,registered_sources=len(sources),pages_with_selected_sources=sum(bool(x['selected_source_ids']) for x in reviews.values()),native_validation_scope='Source registry and all quotations/passage translations; not global translation finalization.',official_semantic_convergence=False,wiki_writes=False)
(O/'selected-integrity-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
