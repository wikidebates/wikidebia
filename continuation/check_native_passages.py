from pathlib import Path
import json,sys
import mwparserfromhell as mw
O=Path(__file__).parent;V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee')
sys.path.insert(0,'/workspace/work/cannabis-correction-relecture/kit/scripts')
from wikidebia_render import _citation_template,_sequence
pending=json.loads((O/'native-import.pending.json').read_text());notes=json.loads((V/'data/translation_editorial_notes.json').read_text());qs=json.loads((V/'data/translation_quotes.json').read_text());findings=[]
for note in notes:
 rec=next(r for r in pending['records'] if r['delivery_id']==note['page_id'])
 quote=next(q for q in rec['quotes'] if q['delivery_quote_id']==note['before_quote_id'])
 passages=rec.setdefault('editorial_passages_requiring_native_support',[])
 passages.append(dict(id=note['id'],before_build_quote_id=quote['build_quote_id'],source_text=note['source_text'],target_text=note['target_text'],status='preserved_in_delivery_not_yet_representable_in_native_locks'))
 # Exercise the actual native quote renderer without generating a page or forging a lock.
 native=_sequence(_citation_template(dict(id=q['build_quote_id'],parameters=[dict(name=k,value=v) for k,v in q['target_parameters']]),lang='en') for q in rec['quotes'])
 working=(O/'working'/rec['working_target_relative_path']).read_text()
 assert note['target_text'] in working and note['target_text'] not in native
 findings.append(dict(delivery_page_id=note['page_id'],build_node_id=rec['build_node_id'],before_build_quote_id=quote['build_quote_id'],passage_id=note['id'],native_citation_sequence_loses_editorial_passage=True,working_draft_preserves_passage=True))
(O/'native-import.pending.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2)+'\n')
(O/'native-editorial-passages-preflight.json').write_text(json.dumps(dict(status='blocked_to_prevent_two_editorial_passage_omissions',repository_commit='0ab6e46f62f76490a81431b75e02371df08ebc28',findings=findings,code_paths=['kit/scripts/wikidebia_content_review.py:_citation_records/_source_imports','kit/scripts/wikidebia_translation_review.py:_blank_argument/_validate_argument','kit/scripts/wikidebia_render.py:_render_argument'],required_change='Transporter et relire la prose hors modèles Citation, avec ancrage avant/après chaque citation, dans les verrous français/anglais et la convergence ; contrôler ensuite le rendu réel. Ne pas remplacer cette prose par un résumé ni la placer dans une nouvelle Quote.',code_modified=False,official_application_attempted=False),ensure_ascii=False,indent=2)+'\n')
print('Préflight natif : deux passages non représentés dans la séquence de citations actuelle ; conservés dans le brouillon et dans la file d’intégration.')
