import json,hashlib,zipfile,sys,collections
from pathlib import Path
import mwparserfromhell as mw
ROOT=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee')
OUT=Path(__file__).parent
ARCHIVE=Path('/workspace/attachments/73035fc5-b72e-411e-8423-9e59665ed4e7/cannabis_traduction_en_2026-10-21_verifiee-c607dbaa912943318d91916e3d15c408.zip')
FR=Path('/workspace/attachments/c7e55140-52a7-474b-9545-afc46c67458c/cannabis_traduction_graphe_recursif_2026-10-21_audite.zip')
def load(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
checks=[]
def check(name,value,details=None):
 checks.append(dict(check=name,passed=bool(value),details=details))
 assert value,name
check('archive_sha256',sha(ARCHIVE.read_bytes())=='b317df79f35b047af2bdead55c5adbdb33c835fae528ed69f0de78e5d8332eda')
with zipfile.ZipFile(ARCHIVE) as z: check('zip_crc',z.testzip() is None)
fm=load(ROOT/'MANIFEST_SHA256.json'); files=fm['files']
check('all_339_declared_hashes',len(files)==339 and all((ROOT/f['path']).stat().st_size==f['size_bytes'] and sha((ROOT/f['path']).read_bytes())==f['sha256'] for f in files))
check('file_coverage',{f['path'] for f in files}=={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}-{'MANIFEST_SHA256.json'})
with zipfile.ZipFile(FR) as z:
 check('original_french_zip_hash',sha(FR.read_bytes())==load(ROOT/'manifest.json')['source_archive_sha256'])
 check('all_original_french_bytes',all((ROOT/'provenance/source'/f.filename).read_bytes()==z.read(f) for f in z.infolist() if not f.is_dir()))
rows=load(ROOT/'data/translation_pages.json'); qs=load(ROOT/'data/translation_quotes.json')
check('page_count',len(rows)==153)
check('unique_ids_and_titles',len({r['id'] for r in rows})==153 and len({r['canonical_title_en'] for r in rows})==153)
check('page_hashes',all(sha((ROOT/r['source_snapshot_relative_path']).read_bytes())==r['source_sha256'] and sha((ROOT/r['target_relative_path']).read_bytes())==r['target_sha256'] for r in rows))
counts=collections.Counter(); bypage=collections.defaultdict(list)
for q in qs: bypage[q['page_id']].append(q)
for row in rows:
 source=mw.parse((ROOT/row['source_snapshot_relative_path']).read_text())
 target=mw.parse((ROOT/row['target_relative_path']).read_text())
 page=next(t for t in target.filter_templates() if str(t.name).strip() in {'Argument','Debate'})
 frpage=next(t for t in source.filter_templates() if str(t.name).strip() in {'Argument','Débat'})
 if row['id']!='debate':
  frsum=frpage.has('résumé') and bool(str(frpage.get('résumé').value).strip())
  ensum=page.has('summary') and bool(str(page.get('summary').value).strip())
  assert frsum==ensum==row['summary_present_fr']==row['summary_present_en'],row['id']
  counts['summaries' if frsum else 'absent_summaries']+=1
 enquotes=[t for t in target.filter_templates() if str(t.name).strip()=='Quote']
 assert len(enquotes)==len(bypage[row['id']]),row['id']
 for t,q in zip(enquotes,bypage[row['id']]):
  assert [[str(p.name).strip(),str(p.value).strip()] for p in t.params]==q['target_parameters'],q['id']
  old=dict(q['source_parameters']);new=dict(q['target_parameters'])
  for a,b in [('auteurs','authors'),('ouvrage','work'),('édition','publisher'),('lien','link'),('article','article'),('page','page'),('volume','volume'),('numéro','issue'),('localisation','location'),('lieu','place')]:
   assert old.get(a)==new.get(b),(q['id'],a)
  assert 'AI-translated quote' in new['warnings'],q['id']
 counts['quotes']+=len(enquotes)
 assert not page.has('initialisation') and not page.has('initialization')
 assert not page.has('date-création') and not page.has('creation-date')
check('summary_and_quote_counts',dict(counts)==dict(absent_summaries=120,quotes=149,summaries=32),dict(counts))
for pid,phrase in [('A0037','Objection to Jean Costentin:'),('A0116','Not all regular users are dependent.')]:
 check(pid+'_restored_editorial_passage',phrase in (ROOT/f'pages/en/arguments/{pid}.wiki').read_text())
check('not_publication_ready',load(ROOT/'manifest.json')['publication_ready'] is False)
report=dict(schema='wikidebia-translation-takeover-reception-1.0',archive_sha256=sha(ARCHIVE.read_bytes()),checks=checks,official_kit_validation=False,documentation_complete=False,wiki_writes=False)
(OUT/'reception.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(checks_passed=len(checks),counts=dict(counts)),ensure_ascii=False))
