from pathlib import Path
import json,hashlib,sys,collections
ROOT=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee');OUT=Path(__file__).parent
BUILD=Path('/workspace/work/cannabis-correction-relecture/.state/corpus-builds/cannabis')
rows=json.loads((ROOT/'data/translation_pages.json').read_text());prov=json.loads((BUILD/'data/import_provenance.json').read_text())
print('PROV fields',prov['pages'][0])
bykey={}
for r in prov['pages']:
 key=(r['canonical_title'],r['revision_id']);assert key not in bykey
 bykey[key]=r
mapped=[]
for row in rows:
 p=bykey[(row['source_title_fr'],row['source_revision_id'])]
 assert p['sha256']==row['source_sha256']
 mapped.append(dict(delivery_id=row['id'],build_node_id=p.get('page_id') or 'debate',source_title_fr=row['source_title_fr'],source_revision_id=row['source_revision_id'],source_sha256=row['source_sha256'],target_sha256=row['target_sha256'],source_relative_path=row['source_snapshot_relative_path'],target_relative_path=row['target_relative_path'],corpus_id_locked=False))
assert len({r['build_node_id'] for r in mapped})==153
(OUT/'identity-map.json').write_text(json.dumps(dict(schema='wikidebia-translation-takeover-identity-map-1.0',status='matched_title_revision_and_hash_not_yet_locked_corpus',rows=mapped),ensure_ascii=False,indent=2)+'\n')
print('Matched:',len(mapped),'reassigned IDs:',sum(r['delivery_id']!=r['build_node_id'] for r in mapped))
sys.path.insert(0,'/workspace/work/cannabis-correction-relecture/kit/scripts')
from wikidebia_graph_extract import iter_templates,normalize_key
refs=[]
for row in rows:
 text=(ROOT/row['target_relative_path']).read_text()
 for call in iter_templates(text):
  if normalize_key(call.name) in {'quote'}:continue
  if 'référence' in normalize_key(call.name) or normalize_key(call.name).startswith('reference'):
   refs.append(dict(page_id=row['id'],template=call.name,parameters=dict(call.params),raw=call.raw))
(OUT/'inline-reference-inventory.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n')
print('Inline reference templates:',len(refs))
for r in refs:print(r['page_id'],r['template'],str(r['parameters'])[:350])
