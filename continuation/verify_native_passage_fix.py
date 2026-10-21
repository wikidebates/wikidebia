from pathlib import Path
import sys,json
import mwparserfromhell as mw
O=Path(__file__).parent;V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee')
sys.path.insert(0,'/workspace/work/cannabis-interquotation-code/kit/scripts')
from wikidebia_citation_passages import inventory_passages,blank_translations,validate_translations
from wikidebia_render import _render_argument
rows=json.loads((V/'data/translation_pages.json').read_text());notes=json.loads((V/'data/translation_editorial_notes.json').read_text());pending=json.loads((O/'native-import.pending.json').read_text());findings=[]
for note in notes:
 row=next(r for r in rows if r['id']==note['page_id']);rec=next(r for r in pending['records'] if r['delivery_id']==note['page_id'])
 source=mw.parse((V/row['source_snapshot_relative_path']).read_text());page=next(t for t in source.filter_templates() if str(t.name).strip()=='Argument')
 src=inventory_passages(str(page.get('citations').value).strip(),rec['build_node_id']);assert len(src)==1
 assert src[0]['text'].strip()==note['source_text']
 translated=blank_translations(src)
 # The two supplied bilingual passages are actually compared here, not auto-attested in bulk.
 text=src[0]['text'];prefix=text[:len(text)-len(text.lstrip())];suffix=text[len(text.rstrip()):]
 translated[0].update(text=prefix+note['target_text']+suffix,equivalent_to_french=True,review_note=('Comparaison du passage français et anglais fourni : opposition à Costentin et alternative occultés/sous-estimés conservées.' if note['id']=='N001' else 'Contradiction seulement apparente, distinction dépendance/usage régulier et négation partielle Not all conservées ; véracité médicale non attestée.'))
 translated=validate_translations(translated,src,rec['build_node_id'])
 cites=[dict(id=q['build_quote_id'],parameters=[dict(name=k,value=v) for k,v in q['target_parameters']]) for q in rec['quotes']]
 rendered=_render_argument(lang='en',node={'id':rec['build_node_id'],'fr':{},'en':{}},content={'citations':cites,'citation_passages':translated},registry={'graph':{'nodes':[],'edges':[]}},sources={},creation_date='',include_interlanguage=False)
 parsed=mw.parse(rendered);p=next(t for t in parsed.filter_templates() if str(t.name).strip()=='Argument');field=str(p.get('quotes').value);quotes=[str(t) for t in mw.parse(field).filter_templates() if str(t.name).strip()=='Quote'];anchor=next(i for i,c in enumerate(cites) if c['id']==src[0]['before_citation_id'])
 assert note['target_text'] in field
 assert field.index(quotes[anchor-1]) < field.index(note['target_text']) < field.index(quotes[anchor])
 assert len(quotes)==len(cites)
 rec['citation_passages_draft_for_native_review']=translated
 findings.append(dict(page_id=note['page_id'],build_node_id=rec['build_node_id'],passage_id=src[0]['id'],source_text=src[0]['text'],target_text=translated[0]['text'],position_and_quotes_preserved_by_actual_native_renderer=True,official_workflow_applied=False))
(O/'native-import.pending.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2)+'\n')
(O/'native-editorial-passages-fix-verification.json').write_text(json.dumps(dict(status='fixed_in_separate_code_branch_not_merged',code_branch='fix/preserve-interquotation-prose',findings=findings,wiki_writes=False),ensure_ascii=False,indent=2)+'\n')
print('Rendu natif corrigé : les deux passages réels sont conservés avant leur citation cible ; aucune citation perdue.')
