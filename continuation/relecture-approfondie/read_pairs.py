from pathlib import Path
import json,sys,collections
import mwparserfromhell as mw
V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee');W=Path('/workspace/work/cannabis-translation-verification-20261021/working')
if len(sys.argv)>3:W=Path(sys.argv[3])
rows=json.loads(((W if len(sys.argv)>3 else V)/'data/translation_pages.json').read_text())
qs=json.loads((V/'data/translation_quotes.json').read_text())
start=int(sys.argv[1]);end=int(sys.argv[2])
for row in rows[start:end]:
 f=(V/row['source_snapshot_relative_path']).read_text();e=(W/row['target_relative_path']).read_text();fc=mw.parse(f);ec=mw.parse(e)
 fp=next(t for t in fc.filter_templates() if str(t.name).strip() in ['Débat','Argument']);ep=next(t for t in ec.filter_templates() if str(t.name).strip() in ['Debate','Argument'])
 print('\n===',row['id'],'===\nTITLE FR:',row['source_title_fr'],'\nTITLE EN:',row['canonical_title_en'])
 if row['id']=='debate':
  print('INTRO FR:',str(fp.get('introduction').value).strip());print('INTRO EN:',str(ep.get('introduction').value).strip())
 else:
  if fp.has('résumé'):print('SUMMARY FR:',str(fp.get('résumé').value).strip())
  if ep.has('summary'):print('SUMMARY EN:',str(ep.get('summary').value).strip())
  fquotes=[t for t in fc.filter_templates() if str(t.name).strip()=='Citation'];equotes=[t for t in ec.filter_templates() if str(t.name).strip()=='Quote']
  assert len(fquotes)==len(equotes)
  qids=[q['id'] for q in qs if q['page_id']==row['id']]
  for qid,a,b in zip(qids,fquotes,equotes):
   print(qid,'FR:',str(a.get('citation').value).strip());print(qid,'EN:',str(b.get('quote').value).strip())
 frels=[t for t in fc.filter_templates() if str(t.name).strip() in ['Argument pour','Argument contre','Justification','Objection']]
 enrels=[t for t in ec.filter_templates() if str(t.name).strip() in ['Pro argument','Con argument','Justification','Objection']]
 assert len(frels)==len(enrels),(row['id'],len(frels),len(enrels))
 for ft,t in zip(frels,enrels):
  print('REL',str(t.name).strip(),str(t.get('page').value).strip(),'; DISPLAY FR=',str(ft.get('titre-affiché').value).strip() if ft.has('titre-affiché') else '<absent>','; EN=',str(t.get('displayed-title').value).strip() if t.has('displayed-title') else '<absent>')
