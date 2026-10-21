"""Corrections lexicales ciblées, sans toucher à la provenance française."""
from pathlib import Path
import json, hashlib
import mwparserfromhell as mw
R=Path(__file__).parent;W=R/'working';V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee')
def load(p):return json.loads(p.read_text())
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
rows=load(W/'data/translation_pages.json');vocab=load(W/'data/vocabulary_bilingual.json');texts=load(W/'data/translation_texts.json');journal=load(R/'corrections.json')
mapping={v['fr']:v['keyword_en'] for v in vocab};prior=mapping.copy()
mapping.update(Interdiction='ban',Contrôle='control')
used=set();section_used=set()
for r in rows:
 f=next(t for t in mw.parse((V/r['source_snapshot_relative_path']).read_text()).filter_templates() if str(t.name).strip() in {'Débat','Argument'})
 if f.has('rubriques'):section_used.update(x.strip() for x in str(f.get('rubriques').value).split(',') if x.strip())
 if not f.has('mots-clés'):continue
 terms=[x.strip() for x in str(f.get('mots-clés').value).split(',') if x.strip()];used.update(terms)
 expected=', '.join(mapping[t] for t in terms);p=W/r['target_relative_path'];c=mw.parse(p.read_text());t=next(t for t in c.filter_templates() if str(t.name).strip() in {'Debate','Argument'})
 before=str(t.get('keywords').value).strip()
 if before!=expected:
  assert any(x in terms for x in ['Interdiction','Contrôle'])
  old=str(t.get('keywords').value);t.get('keywords').value=old.replace(before,expected);p.write_text(str(c))
  journal['changes'].append(dict(page_id=r['id'],field='keywords',before=before,after=expected,source_evidence=terms,reason='Distinguer Interdiction (ban) de Prohibition et conserver le sens large de Contrôle (control) ; aucun terme source ni ordre supprimé.'))
for v in vocab:
 if v['fr'] in ['Interdiction','Contrôle']:
  assert v['keyword_en']==prior[v['fr']];v['keyword_en']=mapping[v['fr']];v['en']=mapping[v['fr']]
for term in ['Interdiction','Contrôle']:
 assert isinstance(texts['vocabulary'][term],str);texts['vocabulary'][term]=mapping[term]
for r in rows:r['target_sha256']=hashlib.sha256((W/r['target_relative_path']).read_bytes()).hexdigest()
save(W/'data/translation_pages.json',rows);save(W/'data/vocabulary_bilingual.json',vocab);save(W/'data/translation_texts.json',texts);save(R/'corrections.json',journal)
native=dict(status='mapping_candidates_only_not_native_approved_vocabulary',source_native_vocabulary_status='draft_and_empty',keyword_mapping=[dict(fr=t,en=mapping[t]) for t in sorted(used)],section_mapping=[dict(fr=v['fr'],en=v['section_en']) for v in vocab if v['fr'] in section_used],note='Les rubriques et mots-clés ont des espaces de noms distincts. Droit est une rubrique, Loi est un mot-clé ; aucune collision law entre mots-clés réels. Définitions, usages et revue native restent à compléter.')
assert len({x['en'].casefold() for x in native['keyword_mapping']})==len(used)
save(R/'vocabulary-namespace-audit.json',native)
(W/'lecture_integrale_en.wiki').write_text('\n\n'.join('== '+r['canonical_title_en']+' ==\n\n'+(W/r['target_relative_path']).read_text() for r in rows))
print('Corrections :',len(journal['changes']),' ; termes keyword distincts :',len(used))
