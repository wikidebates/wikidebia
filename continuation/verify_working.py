from pathlib import Path
import json,hashlib,sys,re,collections,datetime
import mwparserfromhell as mw
O=Path(__file__).parent;V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee');W=O/'working'
sys.path.insert(0,'/workspace/work/cannabis-correction-relecture/kit/scripts')
from wikidebia_translation_review import _validate_sources
checks=[]
def check(k,x,details=None):checks.append(dict(check=k,passed=bool(x),details=details));assert x,k
load=lambda p:json.loads(p.read_text())
rows=load(V/'data/translation_pages.json');ch=load(O/'documentary-changes.json')['changes'];bych={r['page_id']:r for r in ch};counts=collections.Counter()
check('exact_153_page_coverage',{str(x.relative_to(W)) for x in (W/'pages').rglob('*.wiki')}=={r['target_relative_path'] for r in rows})
for r in rows:
 a=(V/r['target_relative_path']).read_text();b=(W/r['target_relative_path']).read_text();ac=mw.parse(a);bc=mw.parse(b)
 ap=next(t for t in ac.filter_templates() if str(t.name).strip() in ['Argument','Debate']);bp=next(t for t in bc.filter_templates() if str(t.name).strip() in ['Argument','Debate'])
 aq=[str(t) for t in ac.filter_templates() if str(t.name).strip()=='Quote'];bq=[str(t) for t in bc.filter_templates() if str(t.name).strip()=='Quote'];assert aq==bq,r['id'];counts['quotes']+=len(aq)
 edge_names={'Pro argument','Con argument','Justification','Objection'}
 ae=[str(t) for t in ac.filter_templates() if str(t.name).strip() in edge_names];be=[str(t) for t in bc.filter_templates() if str(t.name).strip() in edge_names];assert ae==be,r['id'];counts['relations_including_roots']+=len(ae)
 if r['id']!='debate':
  before=ap.has('summary') and bool(str(ap.get('summary').value).strip());after=bp.has('summary') and bool(str(bp.get('summary').value).strip());assert before==after
  counts['summaries' if before else 'absent_summaries']+=1
  if before:
   left=str(ap.get('summary').value);right=str(bp.get('summary').value)
   # Only the four exact Wikipedia link localisations recorded in the change manifest.
   replacements={
   'A0058':('https://fr.wikipedia.org/wiki/L%C3%A9gislation_sur_le_cannabis French Wikipedia: Législation sur le cannabis','https://en.wikipedia.org/wiki/Legality_of_cannabis English Wikipedia: Legality of cannabis'),
   'A0073':('https://fr.wikipedia.org/wiki/Prohibition_des_drogues#Mise_en_place_d.27une_r.C3.A9glementation_internationale','https://en.wikipedia.org/wiki/Drug_prohibition'),
   'A0125':('https://fr.wikipedia.org/wiki/Prohibition_des_drogues#Mise_en_place_d.27une_r.C3.A9glementation_internationale','https://en.wikipedia.org/wiki/Drug_prohibition'),
   'A0143':('https://fr.wikipedia.org/wiki/Libéralisation_des_drogues French Wikipedia: Libéralisation des drogues','https://en.wikipedia.org/wiki/Drug_liberalization English Wikipedia: Drug liberalization')}
   if r['id'] in replacements:left=left.replace(*replacements[r['id']])
   assert left==right,r['id']
 assert not any(bp.has(k) for k in ['initialization','initialisation','creation-date','date-création'])
 if r['id'] not in bych:assert a==b,r['id']
 for t in bc.filter_templates():
  names=[str(p.name).strip() for p in t.params];assert len(names)==len(set(names)),(r['id'],str(t.name))
 check('page_integrity_'+r['id'],True)
check('all_149_quotes_unchanged',counts['quotes']==149)
check('all_170_relations_including_13_roots_unchanged',counts['relations_including_roots']==170)
check('all_summary_presence_and_prose_preserved',counts['summaries']==32 and counts['absent_summaries']==120,dict(counts))
for pid,s in [('A0037','Objection to Jean Costentin:'),('A0116','Not all regular users are dependent.')]:check(pid+'_editorial_passage_preserved',s in (W/f'pages/en/arguments/{pid}.wiki').read_text())
reg=load(O/'sources_en_working.partial.json');_validate_sources(reg,'cannabis',set());check('real_kit_source_registry_subset_validator',len(reg['sources'])==5)
byid={r['delivery_id']:r['build_node_id'] for r in load(O/'identity-map.json')['rows']};valid=set(byid.values())|{'cannabis'}
check('source_usages_match_mapped_build_ids',all(u['page_id'] in valid for s in reg['sources'] for u in s['usage']))
check('base_delivery_all_original_hashes_unchanged',all(hashlib.sha256((V/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in load(V/'MANIFEST_SHA256.json')['files']))
check('all_153_searches_have_responses',load(O/'documentary-research-by-page.json')['page_count']==153)
manifest=dict(schema='wikidebia-documentary-continuation-file-manifest-1.0',status='working_documentation_incomplete_not_publication_ready',files=[dict(path=str(p.relative_to(W)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size_bytes=p.stat().st_size) for p in sorted(W.rglob('*')) if p.is_file()])
(O/'working-files-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
report=dict(schema='wikidebia-documentary-continuation-integrity-audit-1.0',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),counts=dict(counts),checks_passed=len(checks),checks=checks,changed_pages=len(ch),verified_source_records=5,documentation_complete=False,native_workflow_finalized=False,official_semantic_convergence=False,wiki_writes=False)
(O/'working-integrity-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Contrôles intégrité réussis:',len(checks),'; pages:',len(rows),'; modifiées:',len(ch),'; compteurs:',dict(counts))
