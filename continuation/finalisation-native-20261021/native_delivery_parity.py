"""Independent comparison of the final native render with the reviewed delivery."""
from pathlib import Path
import json,hashlib,sys
import mwparserfromhell as mw
F=Path(__file__).parent;W=F/'working'
S=Path('/workspace/work/cannabis-source-preservation-code')
N=S/'.state/editorial-workspaces/cannabis/EN-CANNABIS-20261021/release-copy'
def load(p):return json.loads(p.read_text())
def main_template(p):return next(t for t in mw.parse(p.read_text()).filter_templates() if str(t.name).strip() in {'Débat','Debate','Argument'})
def val(t,k):return str(t.get(k).value).strip() if t.has(k) else ''
checks=[]
def check(label,condition):
 checks.append(dict(check=label,passed=bool(condition)))
 if not condition:raise AssertionError(label)
identity=load(Path('/workspace/work/cannabis-translation-verification-20261021/identity-map.json'))['rows']
mapping={r['delivery_id']:r for r in identity}
rows=load(W/'data/translation_pages.json');quotes=load(W/'data/translation_quotes.json')
reg=load(N/'data/registre_debat.json');nodes={r['id']:r for r in reg['graph']['nodes']}
provenance=load(N/'data/import_provenance.json')['pages'];summaries=absent=quote_count=relations=0
for row in rows:
 pid=row['id'];nid=mapping[pid]['build_node_id'];s=next(r for r in provenance if r.get('kind')=='debate') if pid=='debate' else next(r for r in provenance if r.get('page_id')==nid)
 check(pid+'_source_revision_and_bytes',s['revision_id']==row['source_revision_id'] and s['sha256']==row['source_sha256'] and hashlib.sha256((N/s['import_path']).read_bytes()).hexdigest()==row['source_sha256'])
 original=main_template(W/row['target_relative_path']);rendered=main_template(N/('output/en/debate/debate.wiki' if pid=='debate' else f'output/en/arguments/{nid}.wiki'))
 title=reg['debate']['pages']['en']['canonical_title'] if pid=='debate' else nodes[nid]['en']['canonical_title']
 check(pid+'_canonical_title',title==row['canonical_title_en'])
 for key in ['summary','summary-warnings','sections','keywords','progress','debate-warnings','argument-warnings','topic','expanded-topic','introduction']:
  check(pid+'_'+key,val(rendered,key)==val(original,key))
 if pid!='debate':
  summaries+=bool(val(rendered,'summary'));absent+=not bool(val(rendered,'summary'))
  check(pid+'_no_french_initialization',not rendered.has('initialization'))
  check(pid+'_independent_english_creation_date',val(rendered,'creation-date')=='2026-10-21')
 qs=[t for t in mw.parse(str(rendered)).filter_templates() if str(t.name).strip()=='Quote']
 local=[q for q in quotes if q['page_id']==pid];check(pid+'_quote_count',len(qs)==len(local))
 for t,q in zip(qs,local):
  check(q['id']+'_full_text',val(t,'quote')==q['target_text'])
  check(q['id']+'_all_parameters',{str(p.name).strip():str(p.value).strip() for p in t.params}==dict(q['target_parameters']))
 quote_count+=len(qs)
 for name in ['Pro argument','Con argument','Justification','Objection']:
  a=[str(t) for t in mw.parse(str(original)).filter_templates() if str(t.name).strip()==name]
  b=[str(t) for t in mw.parse(str(rendered)).filter_templates() if str(t.name).strip()==name]
  def params(calls):return [{str(p.name).strip():str(p.value).strip() for p in mw.parse(text).filter_templates()[0].params} for text in calls]
  check(pid+'_'+name+'_targets_and_contextual_labels',params(a)==params(b));relations+=len(b)
check('153_native_english_pages',len(rows)==153)
check('149_full_native_quotes',quote_count==149)
check('32_native_summaries_120_absences',summaries==32 and absent==120)
check('170_native_contextual_relations',relations==170)
for p in load(W/'data/translation_editorial_notes.json'):
 pid=p['page_id'];nid=mapping[pid]['build_node_id'];text=(N/f'output/en/arguments/{nid}.wiki').read_text();q=next(q for q in quotes if q['id']==p['before_quote_id'])
 check(p['id']+'_native_prose_anchored',p['target_text'] in text and text.index(p['target_text'])<text.index(q['target_text']))
receipt=load(S/'.state/corpus-releases/cannabis/EN-CANNABIS-20261021/release-receipt.json')
check('fresh_archive_all_four_layers_passed',all(r['status']=='passed' and r['errors']==r['warnings']==0 for r in receipt['validation_layers'].values()))
check('no_publication',receipt['publication_started'] is False and receipt['remote_access'] is False)
report=dict(status='passed',checks_passed=len(checks),checks=checks,archive_sha256=receipt['archive_sha256'],counts=receipt['content_inventory_counts'])
(F/'native-delivery-parity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Native parity:',len(checks),'checks passed')
