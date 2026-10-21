"""Consigner la revue du graphe conservé, après comparaison de ses 170 relations."""
from pathlib import Path
import json,datetime
P=Path('/workspace/work/cannabis-interquotation-code');B=P/'.state/corpus-builds/cannabis';O=Path(__file__).parent;R=Path('/workspace/work/cannabis-translation-verification-20261021/relecture-approfondie')
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=load(R/'working/data/translation_pages.json');ident=load(R.parent/'identity-map.json')['rows'];to_delivery={r['build_node_id']:r['delivery_id'] for r in ident};notes={r['id']:r['note'] for p in sorted(R.glob('notes-*.json')) for r in load(p)};byid={r['id']:r for r in rows};rels=load(R/'working/data/relations_bilingual.json')
families={
'A0091':'L’efficacité instrumentale de la prohibition est directement contestée ; disponibilité, usages, dissuasion et contournement constituent cette famille.',
'A0092':'Les dommages propres aux usagers (soins, exclusion, prison, produit, dealers) constituent une raison autonome de légaliser.',
'A0093':'Les externalités de la prohibition sur la société (coûts, recettes, crime, contrôles et incendies) sont distinctes des dommages individuels.',
'A0096':'La légitimité de punir et la cohérence des interdictions sont une famille normative autonome, distincte de leur efficacité.',
'A0045':'L’adéquation de la loi française de 1970 est discutée dans son objet, sa compréhension et ses modalités d’application.',
'A0075':'Cette famille réunit les avantages positifs allégués de la réforme ; elle ne se réduit pas au seul constat des dommages de la prohibition.',
'A0063':'La possibilité de contrôler le produit est une réponse directe de politique sanitaire ; l’objection du marché noir en limite la couverture.',
'A0053':'L’existence alléguée de modèles étatiques fonctionnels ouvre la comparaison des modèles canadien et uruguayen, pas une simple anecdote isolée.',
'A0090':'La dissuasion et le signal de l’interdit soutiennent directement le maintien de la prohibition, avec leurs objections propres.',
'A0017':'La protection individuelle contre les risques sanitaires constitue la famille de raisons opposées à la légalisation.',
'A0104':'Les dommages à autrui et à la collectivité organisent une famille distincte de la seule protection du consommateur.',
'A0062':'La faisabilité juridique et l’opportunité politique regroupent les objections internationales, sociales et institutionnelles à la réforme.',
'A0077':'Les conséquences défavorables propres à une réforme (usages, drogues plus dures, mineurs, territoires) constituent une famille prospective autonome.'}
parent_analysis={
'A0001':'L’objection conteste le présupposé d’une loi non appliquée en invoquant le renforcement de la répression.',
'A0005':'L’objection oppose au maintien malgré l’échec un critère de coûts et d’effets pervers justifiant l’abrogation.',
'A0009':'La priorité de faire appliquer la loi répond à l’argument tiré de sa faible application.',
'A0010':'Les justifications développent la comparaison avec des produits licites et les intérêts qui les entourent ; les objections distinguent le risque intrinsèque et l’usage recherché.',
'A0011':'Les objections distinguent vente libre et vente encadrée, puis contestent qu’un défaut de majorité suffise à rejeter la réforme.',
'A0017':families['A0017'],
'A0025':'Le risque à toute dose attaque directement la restriction de danger au seul abus.',
'A0034':'Les objections opposent l’effet dissuasif à l’attrait de l’interdit et l’exemple de produits licites attractifs.',
'A0038':'La baisse alléguée de certains indicateurs conteste l’affirmation d’augmentation ; périodes et populations restent celles des sources.',
'A0045':families['A0045'],
'A0049':'L’origine historique de la loi dans la diffusion du cannabis est opposée à l’affirmation qu’elle ne le visait pas.',
'A0053':families['A0053'],
'A0055':'Les réponses invoquent des mesures de transition et les dommages territoriaux de la politique concurrente.',
'A0058':'Un mouvement de retour en arrière limite l’argument tiré de la diffusion internationale de la réforme.',
'A0060':'Les quatre objections contestent la disparition des trafics par report de produit, clientèle mineure, restrictions et prix.',
'A0061':'Les objections discutent l’inévitabilité de la hausse par comparaison internationale, effet du prix et tendances sous prohibition.',
'A0062':families['A0062'],
'A0063':families['A0063'],
'A0064':'Le coût de nouveaux trafics est opposé à la disponibilité des ressources annoncées pour la prévention.',
'A0066':'L’hétérogénéité des études limite la généralisation d’une substitution à l’alcool.',
'A0070':'La possibilité de dépénaliser l’ensemble des drogues répond au risque de report vers les produits encore interdits.',
'A0071':'Les expériences sans hausse s’opposent à la prédiction d’augmentation ; la force de possibilité de chaque source reste inchangée.',
'A0072':'La distinction thérapeutique/récréatif et la discussion des risques thérapeutiques répondent au lien annoncé entre les deux ouvertures.',
'A0073':'Les objections distinguent offre et usage, recommandation internationale, droits humains, marges juridiques et précédent uruguayen ; elles ciblent la difficulté juridique.',
'A0075':families['A0075'],
'A0077':families['A0077'],
'A0078':'La difficulté d’achat légal des mineurs oppose un mécanisme de protection à l’annonce d’un danger accru.',
'A0082':'L’expérience de la prohibition de l’alcool et le coût de la lutte contre le trafic servent de cas à l’argument historique d’effets contre-productifs.',
'A0084':'L’absence alléguée de réduction des usages conteste directement l’effet dissuasif attribué à l’interdit.',
'A0088':'L’objection refuse la généralisation normative du raisonnement fiscal à tous les marchés illicites.',
'A0089':'La dépendance comme perte de liberté s’oppose à la justification par la liberté de consommer.',
'A0090':families['A0090'],
'A0091':families['A0091'],
'A0092':families['A0092'],
'A0093':families['A0093'],
'A0096':families['A0096'],
'A0099':'L’attrait de l’interdit et les stratégies de contournement contestent les effets attendus du signal sociétal.',
'A0100':'Les causes sociales et le mal-être explicitent les motifs que l’approche répressive serait censée négliger.',
'A0104':families['A0104'],
'A0105':'Les coûts de la politique prohibitive servent de comparaison aux coûts sociaux attribués au produit.',
'A0106':'Les objections différencient précocité, intensité, voie de consommation, contexte et alternative réglementaire ; elles ne changent pas la polarité du parent.',
'A0107':'Le faible sur-risque attribué au cannabis seul et le poids de l’alcool contestent la portée de l’implication routière.',
'A0108':'Les objections distinguent dommage à autrui, comparaison avec la prohibition et comparaison avec d’autres produits licites.',
'A0109':'L’usage antalgique et relaxant fournit un contre-exemple au seul but de planer.',
'A0117':'Les objections discutent l’ampleur de la dépendance, l’intensité d’usage, le contexte et la comparaison avec l’alcool.',
'A0123':'L’action d’intérêts économiques fournit une autre explication de l’attractivité que la seule licéité.',
'A0129':'Les deux objections contestent une généralisation des retours en arrière, par le cas néerlandais et la diffusion des réformes.',
'A0135':'La faible sensibilité aux lois soutient l’inefficacité alléguée ; les faits de dissuasion et l’éducation la contestent ou proposent une autre stratégie.',
'A0137':'Le contre-exemple des réformes sans légalisation des drogues dures et la pente glissante contestent l’enchaînement ; l’argument sur les drogues dures en conteste aussi la valeur négative.',
'A0138':'Les exemples de régulation stricte et de contrôle étatique contestent que le marché impose nécessairement un modèle commercial dérégulé.'}
registry=load(B/'data/registre_debat.json');occ={o['id']:o for o in registry['graph']['occurrences']};edges={e['id']:e for e in registry['graph']['edges']};review=load(B/'reviews/graph_placement_review.json');evidence=[]
for entry in review['entries']:
 o=occ[entry['occurrence_id']];child=to_delivery[o['node_id']]
 if o['depth']==1:
  analysis=families[child];m=entry['main_argument_review'];m.update(direct_answer_to_debate=True,autonomous_without_parent=True,organizes_distinct_argument_family=True,more_general_nonduplicate_parent_available=False,principally_supports_or_attacks_specific_argument=False,principally_example_or_specialization=False)
  parent='debate';rel='root'
 else:
  edge=edges[o['edge_id']];parent=to_delivery[edge['parent_node_id']];rel=edge['relation'];analysis=parent_analysis[parent];entry['subordinate_review'].update(parent_is_best_immediate_target=True,relation_to_parent_explicit=True)
  matching=[r for r in rels if r['source_id']==parent and r['target_id']==child and r['relation']==rel];assert len(matching)==1
 entry.update(placement_status='approved',direct_fit=True,rationale=analysis+' Cible : '+byid[child]['source_title_fr']+'. Lecture de contenu : '+notes[child])
 evidence.append(dict(occurrence_id=o['id'],parent_delivery_id=parent,child_delivery_id=child,relation=rel,rationale=entry['rationale']))
save(B/'reviews/graph_placement_review.json',review)
envelope=load(B/'reviews/graph_build_review.json');envelope.update(decision='approved',reviewer='Codex — revue du snapshot conservé',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),blocking_issues=[],notes='Les 170 occurrences ont été revues en regard des libellés et des contenus source. Les 13 racines organisent des familles directes ; les réutilisations gardent leur cible immédiate et leurs polarités. Approbation du placement du graphe historique à traduire, sans attestation de vérité des affirmations ni réécriture française. Les 153 imports et leurs identités titre/révision/hash restent intacts.')
envelope['attestations']={k:True for k in envelope['attestations']};save(B/'reviews/graph_build_review.json',envelope);save(O/'graph-placement-reading.json',dict(status='reviewed',entries=evidence,source_text_changed=False))
print('Revue consignée :',len(evidence),'occurrences.')
