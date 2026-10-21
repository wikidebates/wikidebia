"""Sélection par raisonnement : conserve le premier brouillon, crée une nouvelle copie.

Les attestations concernent la contribution du document consulté, pas la vérité
de toutes les assertions historiques ni l'authenticité de leurs citations.
"""
from pathlib import Path
import copy, datetime, hashlib, json, shutil, sys
import mwparserfromhell as mw

O = Path(__file__).parent
R = Path('/workspace/work/cannabis-translation-verification-20261021/relecture-approfondie')
P = Path('/workspace/work/cannabis-interquotation-code')
sys.path.insert(0, str(P/'kit/scripts'))
from wikidebia_render import _source_template
from wikidebia_translation_review import _validate_sources

def load(p): return json.loads(p.read_text())
def save(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
W = O/'working-selected'
assert not W.exists(), 'Copie existante à préserver ; ne pas exécuter deux fois.'
pool = copy.deepcopy(load(O/'sources_en_working.json'))
topics = copy.deepcopy(load(O/'source-topics.json'))
for s in pool['sources']: s['usage'] = []
evidence = {r['id']: r for f in ['specific-source-results.json','targeted-gap-results.json'] for r in load(O/f)}
evidence['clinical-stigma'] = load(O/'clinical-stigma-evidence.json')

def web(topic, eid, title, site, date, authors, note, primary, core=None):
    e = evidence[eid]
    assert e['http_status'] == 200
    sid = 'S930'+str(len([s for s in pool['sources'] if s['id'].startswith('S930')])+1).zfill(2)
    topics[topic] = sid
    link = 'https://europepmc.org/article/MED/'+core['id'] if core else e['final_url']
    pool['sources'].append(dict(id=sid,type='webliography',document_kind=None,language='en',
        metadata=dict(authors=authors,article=None,work=None,volume=None,issue=None,location=None,publisher=None,place=None,date=date,link=link,page=title,site=site,title=None),
        verification=dict(status='verified',verified_at=e['accessed_at'],primary_source=primary,language_verified=True,authorship_checked=True,authorship_verified=bool(authors),notes=[note]),
        usage=[],deduplication_key=link,evidence=dict(url=e['final_url'],response_sha256=e['sha256'],read_scope='abstract_and_bibliographic_record' if core else 'relevant_document_sections',doi=core.get('doi') if core else None)))

web('uruguay-brookings','uruguay-brookings','Uruguay’s cannabis law: Pioneering a new paradigm','Brookings Institution','21 March 2018',['John Hudak','Geoff Ramsey','John Walsh'],
    'Notice et PDF réel lus : résumé exécutif, mécanismes réglementaires, critiques OICS et argument de priorité des droits humains. Le rapport décrit aussi des limites de mise en œuvre et de déplacement du marché noir.',False)
web('who-alcohol','who-alcohol-risk','No level of alcohol consumption is safe for our health','World Health Organization — Regional Office for Europe','4 January 2023',[],
    'Communiqué anglais consulté : cancérogénicité et absence de seuil sans risque pour la santé. Aucune assimilation de toutes les doses à un même risque.',True)
web('euda-policy','euda-policy','Cannabis policy: status and recent developments','European Union Drugs Agency',None,[],
    'Corps historique anglais consulté : définitions, modèles réglementaires, réformes uruguayenne et américaines, tolérance néerlandaise. Les actualités et le corps de synthèse ont des dates différentes ; aucun inventaire mondial à jour en 2026 n’est revendiqué.',False)
web('convention-1988','convention-1988','United Nations Convention against Illicit Traffic in Narcotic Drugs and Psychotropic Substances, 1988','United Nations Office on Drugs and Crime','1988',[],
    'Texte primaire anglais, article 3(2) lu : possession, achat, culture pour consommation personnelle, sous réserves constitutionnelles ; le texte ne nomme pas la consommation elle-même dans cette disposition.',True)
web('fallacies','stanford-fallacies','Fallacies','Stanford Encyclopedia of Philosophy','30 August 2024',['Hans Hansen'],
    'Notice anglaise, auteur et révision vérifiés ; passage sur slippery slope effectivement lu : enchaînement causal contestable et variante par termes vagues. Aucune sous-espèce précise n’est imposée à la page source.',False)
for topic, eid, filename, note in [
    ('crime','crime-paper','crime-paper.body','Résumé anglais et métadonnées lus : panel d’États américains 1990–2006, lois médicales, homicides et agressions. Association possible à une baisse ; aucune preuve causale de toute criminalité après légalisation récréative.'),
    ('clinical-stigma','clinical-stigma','clinical-stigma-core.body','Résumé anglais et métadonnées lus : perspective clinique, héritage de criminalisation, stigmatisation et obstacles au dialogue thérapeutique ; approche des intentions des patients sans jugement. Ce n’est pas une estimation causale des obstacles français.')]:
    c = load(O/'responses'/filename)['resultList']['result'][0]
    web(topic,eid,c['title'].rstrip('.'),'Europe PMC',str(c['pubYear']),[a.get('collectiveName') or a['fullName'] for a in c['authorList']['author']],note,topic=='crime',c)

# Choix manuels après lecture des mécanismes et comparaison au raisonnement de chaque page.
# L'absence dans cette table signifie qu'aucun nouvel ajout documentaire n'est retenu.
selected = {
 'debate':'rand,canada,portugal,service-public',
 'A0002':'aclu','A0003':'traffic-alcohol,traffic-original','A0004':'use-route',
 'A0007':'uruguay-brookings','A0008':'rand','A0010':'relative-harm,dependence',
 'A0012':'youth-europe,uruguay','A0013':'youth-europe','A0014':'equity',
 'A0016':'use-route','A0017':'early-use,psychosis','A0018':'mill',
 'A0021':'rand','A0022':'youth-europe','A0023':'product-contaminants',
 'A0024':'nida','A0026':'relative-harm,dependence','A0029':'food-industry',
 'A0031':'rand','A0032':'euda-policy','A0033':'rand',
 'A0037':'medical-benefits','A0038':'france','A0039':'relative-harm',
 'A0040':'context-addiction','A0041':'aclu','A0042':'nida',
 'A0053':'canada,uruguay-brookings','A0054':'canada','A0056':'rand',
 'A0057':'rand','A0058':'euda-policy','A0060':'rand,canada',
 'A0061':'youth-europe,uruguay','A0062':'uruguay-brookings',
 'A0063':'canada,product-contaminants','A0064':'rand','A0065':'aclu',
 'A0066':'alcohol-substitute','A0067':'crime',
 'A0068':'opioid-original,opioid-reversal','A0069':'opioid-original,opioid-reversal',
 'A0071':'youth-europe','A0073':'convention,convention-1988,uruguay-brookings',
 'A0075':'rand,canada','A0076':'convention','A0077':'youth-europe,canada',
 'A0078':'early-use,use-route','A0082':'rand','A0083':'rand',
 'A0084':'youth-europe','A0085':'clinical-stigma','A0086':'aclu',
 'A0087':'rand','A0088':'rand','A0089':'mill','A0090':'youth-europe',
 'A0091':'youth-europe','A0092':'aclu,clinical-stigma','A0093':'rand,aclu',
 'A0094':'rand','A0096':'mill,relative-harm','A0097':'canada,product-contaminants',
 'A0100':'clinical-stigma','A0102':'uruguay-brookings','A0103':'aclu',
 'A0104':'traffic-risk','A0105':'rand','A0106':'nida,psychosis,early-use',
 'A0107':'traffic-risk,traffic-alcohol','A0108':'traffic-alcohol,rand',
 'A0110':'medical-benefits','A0111':'traffic-alcohol','A0113':'traffic-risk,traffic-original',
 'A0114':'purdue','A0115':'portugal','A0116':'dependence','A0117':'nida,dependence',
 'A0118':'dependence,use-route','A0119':'commercialisation,rand',
 'A0120':'uruguay-brookings','A0121':'rand','A0122':'low-tobacco,who-alcohol',
 'A0124':'youth-europe','A0125':'convention-1988,portugal',
 'A0126':'uruguay-brookings','A0128':'industry-alcohol','A0129':'dutch',
 'A0130':'euda-policy','A0131':'dutch','A0133':'relative-harm,dependence',
 'A0134':'early-use,use-route,nida','A0135':'youth-europe','A0136':'alcohol-substitute',
 'A0138':'rand','A0140':'canada','A0141':'use-route,nida',
 'A0142':'portugal','A0143':'portugal','A0144':'dutch,rand',
 'A0146':'rand','A0147':'rand','A0148':'fallacies',
 'A0151':'rand,canada','A0152':'canada-law,uruguay-brookings',
}
reasons = {
 'A0007':'Le rapport Brookings développe le dispositif uruguayen : État, autoculture, clubs, pharmacies, limites et publicité ; la seule enquête adolescente est écartée de cette justification réglementaire.',
 'A0014':'L’étude de cinq États développe les licences, réparations et réinvestissements comme mécanismes de transition inclusive. Elle n’authentifie pas les 260 000 emplois de la source française.',
 'A0021':'RAND développe explicitement la demande exclue par l’âge, le détournement vers les mineurs et les limites de la régulation ; ce mécanisme étaye une persistance possible du marché illicite sans prouver always/never.',
 'A0024':'La page NIDA explique le trouble de l’usage et les signes cliniques ; c’est la prémisse sanitaire du raisonnement, pas une justification génétique déterministe ni une preuve de l’illégitimité de toute peine.',
 'A0032':'EUDA compare des modèles et définitions juridiques différents ; ces variations étayent la contingence des normes, sans prétendre inventorier toutes les cultures.',
 'A0042':'NIDA décrit perte de contrôle et poursuite malgré les dommages, mécanisme clinique pertinent pour la prémisse de dépendance ; la conclusion philosophique de servitude demeure celle de la citation.',
 'A0057':'RAND analyse la concentration des ventes sur les consommateurs fréquents, les incitations commerciales et le lobbying : développement du mécanisme économique, avec solutions réglementaires concurrentes.',
 'A0058':'Le corps historique EUDA documente les réformes américaines et uruguayenne en distinguant légalisation, dépénalisation et tolérance. Il ne valide ni la carte de 2024 ni un décompte actuel de tous les pays.',
 'A0062':'Brookings développe précisément l’obstacle des conventions et la réponse uruguayenne ; c’est le volet juridique du raisonnement, pas une preuve que toute légalisation serait indésirable.',
 'A0064':'RAND met en relation taxes, recettes et financement/coûts de régulation. Le mécanisme budgétaire est développé, sans garantie d’affectation effective à la prévention.',
 'A0067':'Morris et ses coauteurs analysent l’hypothèse de baisse des crimes et les résultats américains sous lois médicales ; résultats bornés à 1990–2006 et aux infractions étudiées.',
 'A0068':'Bachhuber développe l’hypothèse de substitution aux opioïdes et l’association initiale ; Shover reprend ce même mécanisme puis examine sa non-réplication et le risque de confusion écologique.',
 'A0069':'Les deux études développent le mécanisme de substitution et de mortalité pour les opioïdes ; cette composante de l’argument ne prouve pas le même effet pour toutes les autres drogues.',
 'A0073':'Lecture des articles pertinents des conventions de 1961 amendée et 1988, puis analyse Brookings de la tension entre légalisation uruguayenne et obligations : contraintes, réserves et réponses sont distinguées.',
 'A0076':'Article 4 : limitation aux fins médicales et scientifiques ; article 36 : réserves constitutionnelles. Cela développe une marge liée aux fins scientifiques, sans transformer une expérience commerciale en autorisation générale.',
 'A0085':'La perspective clinique Smith–Sera développe les obstacles au dialogue et à la confiance liés à la stigmatisation et à l’héritage de la prohibition ; elle ne chiffre pas un effet français.',
 'A0094':'RAND p. 46 développe la séparation néerlandaise des marchés : obtenir du cannabis sans rencontrer les vendeurs de drogues dures. C’est un mécanisme social distinct d’une passerelle pharmacologique.',
 'A0097':'Le bilan canadien développe les exigences de contrôle et l’intérêt d’analyser les produits saisis ; la revue analytique développe les méthodes de détection. Aucun contrôle n’est présenté comme garantie absolue.',
 'A0100':'Smith–Sera développe l’exploration des intentions et expériences du patient plutôt qu’une lecture punitive ; cette démarche étaye la prise en compte des motifs, sans diagnostiquer chaque usager.',
 'A0102':'Brookings examine le modèle uruguayen et ses résultats/limites de mise en œuvre ; aucune élimination quasi complète du marché noir n’est déclarée vérifiée.',
 'A0103':'Le rapport ACLU développe les conséquences des arrestations et amendes sur emploi, logement et personnes pauvres : mécanisme social pertinent, avec limite au contexte américain.',
 'A0111':'Martin et ses coauteurs analysent le risque routier et la co-consommation alcool/cannabis. Cette composante de l’interaction est développée ; les effets conjoints avec le tabac ne sont pas déclarés vérifiés.',
 'A0120':'Brookings expose expressément la défense uruguayenne fondée sur la priorité des droits humains face au régime de contrôle des drogues ; l’argument est documenté comme position juridique, sans jugement définitif de hiérarchie.',
 'A0121':'RAND p. 62 développe la publicité, les marques et l’innovation comme incitations à la consommation, avec exemples alcool/tabac ; le mécanisme d’attrait est distingué de la simple licéité.',
 'A0122':'Hackshaw développe les risques cardiovasculaires du tabac même à faible dose ; le communiqué OMS développe le risque de cancer de l’alcool sans seuil sûr. Deux mécanismes sanitaires, sans taux universel commun.',
 'A0124':'L’étude européenne examine les effets selon fréquence et constate des effets non détectés sur les usagers fréquents ; cela étaye la limite de certaines sanctions, sans vérifier le cas de la peine de mort.',
 'A0125':'L’article 3(2) de 1988 distingue possession/achat/culture pour consommation personnelle et consommation elle-même ; le rapport portugais développe la réponse administrative, sans légalisation du trafic.',
 'A0126':'Brookings relate directement les critiques OICS et l’adoption/mise en œuvre uruguayenne ; la référence documente le nouveau titre prudent, pas l’ancienne affirmation d’absence de critiques.',
 'A0130':'EUDA décrit historiquement la diffusion de plusieurs réformes ; l’évolution du nombre de juridictions est documentée dans cette période, sans inventaire mondial en 2026.',
 'A0140':'Le panel canadien développe la nécessité de maintenir un programme médical distinct du circuit non médical : séparation des régimes et suivi clinique, pas simple constat d’efficacité thérapeutique.',
 'A0143':'Le rapport Portugal développe la dépénalisation de l’usage personnel évoquée dans le résumé. Il n’est pas transformé en preuve de légalisation générale, ni en vérification de toute la liste internationale.',
 'A0144':'Les contrôles d’identité néerlandais et les scénarios RAND de vérification d’âge développent le mécanisme de restriction en magasin ; ils ne prouvent pas une impossibilité absolue d’accès pour un mineur.',
 'A0148':'La notice spécialisée de Hansen développe le raisonnement par chaîne de conséquences et l’insuffisance de ses maillons ; elle documente le sophisme sans inventer d’appellation supplémentaire.',
 'A0152':'La loi canadienne et le dispositif uruguayen Brookings développent les limites légales à la promotion et à la distribution ; leur efficacité totale n’est pas postulée.'
}

old_choices = {}
for line in (O/'page_choices.tsv').read_text().splitlines():
    pid, ts, note = line.split('\t',2); old_choices[pid] = (ts.split(',') if ts else [], note)
identity = load(R.parent/'identity-map.json')['rows']
ids = {r['delivery_id']:r['build_node_id'] for r in identity}; ids['debate'] = 'cannabis'
rows = load(R/'working/data/translation_pages.json')
notes = {n['id']:n['note'] for p in sorted(R.glob('notes-*.json')) for n in load(p)}
by_source = {s['id']:s for s in pool['sources']}
sources_by_topic = {k:by_source[v] for k,v in topics.items()}
shutil.copytree(R/'working',W)
reviews=[];changes=[]
for row in rows:
    pid=row['id']; chosen=selected.get(pid,'').split(',') if selected.get(pid) else []
    prev_topics, oldnote=old_choices[pid]
    note=reasons.get(pid,oldnote) if chosen else 'Aucun ajout retenu : les documents trouvés ne développent pas suffisamment ce raisonnement particulier. '+oldnote
    path=W/row['target_relative_path']; before=path.read_text(); code=mw.parse(before)
    main=next(t for t in code.filter_templates() if str(t.name).strip() in {'Debate','Argument'})
    selected_ids=[topics[t] for t in chosen]
    if pid!='debate':
        for bucket in ['bibliography','webliography','videography']:
            if main.has(bucket):main.remove(bucket)
        for bucket in ['bibliography','webliography','videography']:
            matching=[sources_by_topic[t] for t in chosen if sources_by_topic[t]['type']==bucket]
            if matching:main.add(bucket,'\n'+''.join(_source_template(s,lang='en')+'\n' for s in matching),preserve_spacing=False)
    for topic in chosen:
        s=sources_by_topic[topic]
        use=dict(page_id=ids[pid],language='en',role='neutral_reference' if pid=='debate' else 'supports_summary',selection_reason=note)
        if pid=='debate' and s['type']=='bibliography':use['documentary_scope']='broad_synthesis'
        if pid!='debate':
            use.update(argument_development_verified=True,
                also_develops_objections=topic in {'rand','canada','youth-europe','alcohol-substitute','opioid-reversal','medical-benefits','use-route','uruguay-brookings','euda-policy','mill','crime','fallacies','clinical-stigma','dependence','psychosis'})
        s['usage'].append(use)
    after=str(code)
    if after!=before:path.write_text(after);changes.append(dict(page_id=pid,fields=['bibliography','webliography','videography'],selected_source_ids=selected_ids))
    row['pre_documentary_completion_sha256']=row['target_sha256'];row['target_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    row['documentary_status']='page_selection_reviewed_authenticity_and_native_gates_open';row['publication_ready']=False
    reviews.append(dict(delivery_id=pid,native_id=ids[pid],source_title_fr=row['source_title_fr'],source_revision_id=row['source_revision_id'],source_sha256=row['source_sha256'],selected_source_ids=selected_ids,selected_topics=chosen,rejected_draft_topics=sorted(set(prev_topics)-set(chosen)),selection_note=note,textual_review_note=notes[pid],documentary_selection_reviewed=True,quotation_authenticity_fully_verified=False,native_lot_closed=False,reviewer='Codex — sélection documentaire par raisonnement',reviewed_at=now))
pool['sources']=[s for s in pool['sources'] if s['usage']]
pool['status']='selected_by_reasoning_native_finalization_pending'
pool['verification_scope']='Source identity, stated language, metadata and specified consulted sections; not all historical claims or quotations.'
_validate_sources(pool,'cannabis',set())
save(O/'sources_en_selected.json',pool);save(O/'source-topics-selected.json',topics)
save(O/'page-documentary-selection-final.json',dict(page_count=153,rows=reviews,native_workflow_finalized=False,discarded_intermediate='working/ — brouillon documentaire contextuel non livrable'))
save(O/'documentary-changes-selected.json',dict(changes=changes,french_changed=False,summaries_changed=False,quotes_changed=False))
save(W/'data/sources_en_working.json',pool);save(W/'data/translation_pages.json',rows)
(W/'lecture_integrale_en.wiki').write_text('\n\n'.join('== '+r['canonical_title_en']+' ==\n\n'+(W/r['target_relative_path']).read_text() for r in rows))
m=load(W/'manifest.json');m.update(status='text_reviewed_documentation_selected_native_gates_open',registered_sources=len(pool['sources']),documentary_page_selection_count=153,publication_ready=False);save(W/'manifest.json',m)
print(json.dumps(dict(sources=len(pool['sources']),pages_with_selected_sources=sum(bool(r['selected_source_ids']) for r in reviews),documentary_page_changes=len(changes),native_source_registry_subset='passed',publication_ready=False)))
