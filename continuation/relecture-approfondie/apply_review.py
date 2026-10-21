from pathlib import Path
import json,shutil,hashlib,csv,copy
import mwparserfromhell as mw
O=Path(__file__).parent;V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee');OLD=O.parent/'working';W=O/'working'
assert not W.exists(), 'Ne pas écraser une copie existante'
shutil.copytree(OLD,W)
rows=json.loads((W/'data/translation_pages.json').read_text());texts=json.loads((W/'data/translation_texts.json').read_text());quotes=json.loads((W/'data/translation_quotes.json').read_text());changes=[]
def record(pid,kind,before,after,reason,source):
 changes.append(dict(page_id=pid,field=kind,before=before,after=after,reason=reason,source_evidence=source))
renames={
 'A0079':('Clandestine cannabis cultivation causes many fires','Clandestine cannabis production causes many fires','Production source non limitée à la culture.'),
 'A0087':('Cannabis prohibition creates a lucrative underground economy with corruption, money laundering, youth recruitment, violence, insecurity and arms trafficking','Cannabis prohibition creates a highly lucrative underground economy with corruption, money laundering, youth recruitment, violence, insecurity and arms trafficking','Degré très lucrative conservé par highly lucrative.'),
 'A0103':('Punitive drug policies can burden vulnerable people and prisons','Punitive drug policies can burden people in precarious circumstances and prisons','Personnes précaires ne désigne pas toutes les vulnérabilités.')}
summary_edits={
 'A0006':('decriminalising abortion and homosexuality','decriminalising abortion or homosexuality','Coordination ou conservée entre exemples, sans modifier les exemples eux-mêmes.','la dépénalisation de l’IVG ou de l’homosexualité'),
 'A0143':('such as Portugal and the Czech Republic','such as Portugal or the Czech Republic','Coordination illustrative ou conservée.','Certains pays comme le Portugal ou la République tchèque')}
quote_edits={
 'Q042':('In 2010, the worst year on record,','In 2010, the year with the worst figures,','Retrait de on record qui étend la portée temporelle au-delà de la formulation source.','En 2010, année affichant les pires chiffres'),
 'Q044':('https://fr.wikipedia.org/wiki/Weather_Underground','https://en.wikipedia.org/wiki/Weather_Underground','Localisation du lien dans le texte traduit, cible anglaise consultée et vérifiée ; le paramètre link de la citation est inchangé.','Weather Underground dans le texte source'),
 'Q047':('habituation','dependency','Assuétude désigne ici la dépendance, pas la seule accoutumance ; liste de synonymes source conservée.','dépendance, addiction, assuétude, esclavage'),
 'Q078':('and that homosexuality was once a crime','or that homosexuality was once a crime','Coordination source ou conservée.','ou que l’homosexualité fut un crime'),
 'Q093':('and that homosexuality was once a crime','or that homosexuality was once a crime','Même passage source que Q078 ; même coordination conservée.','ou que l’homosexualité fut un crime'),
 'Q114':('Expanding the range of legal drugs would cause far more deaths','Expanding the range of legal drugs would mean much greater lethality','Conserver la létalité sans la remplacer par un nombre absolu de décès ni renforcer le lien causal.','En élargissant la palette des drogues licites, la létalité serait bien supérieure')}
qby={q['id']:q for q in quotes}
for pid,(before,after,reason) in renames.items():
 row=next(r for r in rows if r['id']==pid);assert row['canonical_title_en']==before
 row['canonical_title_en']=after;texts['canonical_titles'][pid]=after;record(pid,'canonical_title',before,after,reason,row['source_title_fr'])
 assert len(after.encode())<=255 and '’' not in after
for row in rows:
 pid=row['id'];path=W/row['target_relative_path'];body=path.read_text();code=mw.parse(body);page=next(t for t in code.filter_templates() if str(t.name).strip() in ['Argument','Debate'])
 if pid=='debate':
  subsection=next(t for t in code.filter_templates() if str(t.name).strip()=='Subsection');assert str(subsection.get('title').value).strip()=='The question';subsection.remove('title');record(pid,'subsection[0].title','The question',None,'Préserver l’absence de titre de la sous-partie française historique.','Premier modèle Sous-partie sans titre')
 if pid in summary_edits:
  a,b,reason,source=summary_edits[pid];value=str(page.get('summary').value);assert value.count(a)==1;page.get('summary').value=value.replace(a,b);record(pid,'summary',a,b,reason,source)
 pquotes=[t for t in code.filter_templates() if str(t.name).strip()=='Quote'];dataquotes=[q for q in quotes if q['page_id']==pid];assert len(pquotes)==len(dataquotes)
 for t,q in zip(pquotes,dataquotes):
  if q['id'] not in quote_edits:continue
  a,b,reason,source=quote_edits[q['id']];value=str(t.get('quote').value);assert value.count(a)==1;t.get('quote').value=value.replace(a,b);new=str(t.get('quote').value).strip();q['target_text']=new
  for p in q['target_parameters']:
   if p[0]=='quote':p[1]=new
  texts['quote_texts'][q['id']]=new
  record(pid,q['id']+'.quote',a,b,reason,source)
 body=str(code)
 for a,b,_ in renames.values():body=body.replace(a,b)
 path.write_text(body);row['previous_working_target_sha256']=row['target_sha256'];row['target_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
 page=next(t for t in mw.parse(body).filter_templates() if str(t.name).strip() in ['Argument','Debate'])
 if pid in texts['summaries']:texts['summaries'][pid]=str(page.get('summary').value).strip()
 if pid=='debate':texts['introduction_after_documentary_localization']=str(page.get('introduction').value).strip()
# Only target-language title values are replaced; source provenance and actual query logs are immutable.
def renamed(v):
 if isinstance(v,str):
  for a,b,_ in renames.values():
   if v==a:return b
  return v
 if isinstance(v,list):return [renamed(x) for x in v]
 if isinstance(v,dict):return {k:renamed(x) for k,x in v.items()}
 return v
for n in ['labels_bilingual.json','relations_bilingual.json']:
 p=W/'data'/n;p.write_text(json.dumps(renamed(json.loads(p.read_text())),ensure_ascii=False,indent=2)+'\n')
texts=renamed(texts)
for n,d in [('translation_pages.json',rows),('translation_texts.json',texts),('translation_quotes.json',quotes)]:
 (W/'data'/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(W/'lecture_integrale_en.wiki').write_text('\n\n'.join('== '+r['canonical_title_en']+' ==\n\n'+(W/r['target_relative_path']).read_text() for r in rows))
with (W/'data/titres_bilingues_relecture.csv').open('w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['delivery_id','title_fr','title_en','source_revision']);writer.writerows([r['id'],r['source_title_fr'],r['canonical_title_en'],r['source_revision_id']] for r in rows)
manifest=json.loads((W/'manifest.json').read_text());manifest.update(status='bilingual_text_reread_documentation_and_native_reviews_incomplete',text_reviewed_page_count=153,publication_ready=False);(W/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
report=dict(schema='wikidebia-detailed-bilingual-review-corrections-1.0',changes=changes,source_french_changed=False,quote_metadata_changed=False,summary_additions=0,quote_deletions=0,relations_changed=False,publication=False)
(O/'corrections.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Corrections ciblées :',len(changes),'sur',len({r['page_id'] for r in changes}),'fiches (plus liens entrants des trois titres).')
