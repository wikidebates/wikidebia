# Diagnostic cannabis : noms français et titres anglais

La livraison concernée est `cannabis_traduction_en_2026-10-21_finalisee.zip`,
SHA-256 `fbb70744a0b0d67fdf4a556999cebb038babf754386a7ca6fca43584a6340cf4`.
Les identifiants ci-dessous sont ceux du corpus natif, distincts des identifiants
locaux de la livraison de traduction précédente.

## Trois liens interlangues français bloqués

Le journal transmis par le propriétaire confirme la publication anglaise :
59 créations et 94 pages équivalentes. Le plan français suivant contient
150 mises à jour et trois blocages pour page absente ; ce plan bloqué n’a pas
exécuté les mises à jour françaises.

Dans A0028, A0030 et A0066, le manifeste et le verrou français portent une
apostrophe droite alors que la provenance conserve le nom exact avec `’` :
respectivement `l’univers`, `blanchiment d’argent` et `l’alcool`.
`wikidebia_corpus_init.normalize_title()` effectue cette substitution lors de
la construction du graphe. Elle ne constitue pas un renommage MediaWiki.
L’updater recherchait pourtant exclusivement le nom du manifeste.

Le correctif ajoute une résolution limitée à `interlanguage_only`, depuis la
provenance et le fichier importé vérifié. Il exige une identité de révision et
de contenu, ou le seul lien attendu déjà ajouté. Il conserve le nom exact dans
le plan et l’état publié. Les autres écarts ne sont pas adoptés implicitement.
Les trois cas réels font l’objet de tests d’exécution et de reprise.

Ce correctif ne normalise pas rétroactivement tous les titres français, ne
renomme pas le wiki et ne réécrit pas la livraison historique.

## Titres anglais à rouvrir

L’inventaire exhaustif des titres canoniques de l’archive trouve quatre titres
avec un point intérieur suivi d’une nouvelle phrase ou un point-virgule :

- A0099 : `Alcohol and tobacco are not inherently dangerous; only excessive use is` ;
- A0124 : `The addictive potential of cannabis is neither inherently low nor high; it depends on the level of use` ;
- A0125 : `Drug dependence is not independent of the person and their environment. Drugs are a way of coping with life, not the cause of dependence` ;
- A0150 : `The law is not only enforced; enforcement has intensified since 2001`.

Le contrôle `_title_format_issues()` de la revue de traduction retourne une
liste vide pour chacun. Il teste les guillemets, apostrophes, points de
suspension et point final, pas la juxtaposition de propositions ou phrases.
Le contrôle `WDV-GRA-016` du validateur présente la même lacune pour ce défaut.

Les notes natives des quatre pages attestent la conservation de leur sens
français. Le script de préparation `complete_native_review.py` attribue ensuite
collectivement les booléens de fidélité et de qualité `FIDELITY`, dont
`title_is_idiomatic`, à toutes les fiches. La revue a donc enregistré ces titres
comme approuvés sans relever leur construction. Les contrôles techniques et
ces attestations ne prouvaient pas une qualité éditoriale suffisante.

La préservation des libellés affichés historiques ne rend pas intangible un
nom de page canonique. Elle ne doit pas être étendue à une dispense de revue
éditoriale du titre canonique. Les règles actuelles encadrent l’autonomie et
la typographie mais n’ont pas de garde spécifique contre ce défaut.

La demande du propriétaire impose de rouvrir cette revue et de traiter
explicitement les noms français et anglais concernés. Cette investigation
n’a ni renommé ces pages ni modifié leurs citations ou résumés, et n’a pas
requalifié silencieusement les anciens reçus de convergence en nouvelle revue.

## Correctif préparé après accord du propriétaire

La garde partagée `wikidebia_title_structure.py` est maintenant appelée dans
la revue française, la revue anglaise et sa garde pré-application, le publisher
et les créations/déplacements de l'updater. L'exécuteur relit également les
titres des anciens plans signés avant leur application. Elle ne s'applique pas
rétroactivement aux libellés affichés historiques ou à un ajout pur de lien
interlangue. Les limites de l'heuristique et le besoin de vraie revue de sens
sont explicités dans `GUIDE_CANONICAL_TITLE_REVIEW.md`.

Les huit nouveaux noms et leurs justifications individuelles sont conservés
dans `tests/fixtures/cannabis_title_corrections_20261022.json`. La comparaison
avec le ZIP historique vérifie la correspondance des anciens noms et l'absence
de collision dans le corpus. Douze cibles de relations ou liens interlangues
sont inventoriées pour une reprise ultérieure, sans réécrire leurs libellés.
Cette préparation n'est pas une nouvelle archive `release_ready` : les contrôles
distants, renommages et nouveaux verrous et reçus restent nécessaires.

## Accès externes de cette investigation

La tentative GitHub retourne HTTP 401 `Bad credentials`; Git HTTPS n’a pas
d’identifiant utilisable. Aucun push, fusion ou déploiement de ces correctifs
n’est attesté. Les appels de lecture aux API publiques FR et EN ont reçu HTTP
403 ; le diagnostic des blocages utilise le plan transmis par le propriétaire
et les fichiers de provenance, pas une lecture distante prétendument réussie.
