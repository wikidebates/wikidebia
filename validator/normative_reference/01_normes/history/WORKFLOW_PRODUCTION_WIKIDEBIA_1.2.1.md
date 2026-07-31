# Workflow de production des débats de Wikidéb'IA

- **Version du workflow :** 1.0
- **Révision corrective du paquet :** 1.0.6
- **Version de structure MediaWiki compatible :** 1.0
- **Version de profil de rendu compatible :** 1.0
- **Version du registre compatible :** 1.0
- **Date de validation de cette version :** 2026-07-23
- **Statut :** source normative
- **Dépendances :**
  - `cahier_des_charges_consolide_wikidebia.md`
  - `requirements_catalog_wikidebia.json`
  - `structures_mediawiki_wikidebia.md`
  - `profils_rendu_wikidebia.md`
  - `schema_graphe_registre_wikidebia.md`
  - `modele_registre_debat_wikidebia.json`

## 1. Fonction de ce document

Ce document définit l'architecture opérationnelle complète permettant de produire, valider, publier et archiver un débat Wikidéb'IA.

Il fixe :

- la liste exacte des types de Work ;
- l'ordre des étapes ;
- les entrées et sorties de chaque Work ;
- les conditions de démarrage et de réussite ;
- les champs et fichiers qu'un Work peut modifier ;
- les règles de transmission entre Work ;
- la production par lots ;
- les verrouillages successifs ;
- les procédures de validation française, anglaise et bilingue ;
- l'intégration initiale des liens interlangues français ;
- l'ordre de publication ;
- la procédure de clôture et d'archivage ;
- les conventions de nommage des conversations et fichiers ;
- les mesures destinées à limiter la perte de qualité et les erreurs de contexte.

Ce workflow est conçu pour être répété sur plusieurs centaines de débats.

---

# 2. Organisation des Projets ChatGPT

## 2.1 Projet actif

Nom :

```text
Wikidéb'IA
```

Il contient uniquement :

- les sources normatives et leurs versions actuelles ;
- les prompts Work maîtres ;
- les outils et scripts communs ;
- les conversations consacrées au débat actif ;
- les fichiers du débat actif nécessaires aux Work en cours.

Un seul débat principal doit normalement être en production à la fois dans le projet actif. Une exception peut être décidée manuellement, mais les fichiers doivent alors être strictement séparés par `debate_id`.

## 2.2 Projet d'archives

Nom :

```text
Archives de Wikidéb'IA
```

Il reçoit, après clôture :

- toutes les conversations Work du débat ;
- le paquet final du débat ;
- les rapports de validation ;
- les journaux d'import ;
- les migrations ;
- le rapport de publication et d'archivage.

Il faut déplacer les conversations dans le projet d'archives. La fonction générale d'archivage d'une conversation ne remplace pas ce déplacement.

## 2.3 Sources permanentes et fichiers temporaires

Les sources normatives restent dans le projet actif :

```text
structures_mediawiki_wikidebia.md
profils_rendu_wikidebia.md
schema_graphe_registre_wikidebia.md
workflow_production_wikidebia.md
schemas JSON
prompts Work maîtres
validateur stable
scripts Pywikibot communs
```

Les fichiers propres à un débat sont retirés du projet actif après clôture.

---

# 3. Principes d'exécution

## 3.1 Des Work autonomes et de même niveau

Un Work ne contient pas d'autres Work.

Chaque Work est une conversation autonome, spécialisée dans une tâche intellectuelle déterminée.

Les Work communiquent exclusivement par des fichiers validés. Le souvenir d'une conversation précédente ou le contexte implicite du projet ne constitue jamais une source de vérité structurelle.

## 3.2 Une seule étape responsable de chaque donnée

Chaque donnée possède une étape propriétaire.

| Donnée | Étape propriétaire |
|---|---|
| Cadrage du débat | Work 00 |
| Nœuds, relations, occurrences et titres canoniques français et anglais | Work 01 |
| Page Débat française | Work 02 |
| Contenu des pages Argument françaises | Work 03 par lots |
| Validation française globale | Work 04 |
| Audit bilingue des titres et métadonnées anglaises | Work 05 |
| Page Debate anglaise | Work 06 |
| Contenu des pages Argument anglaises | Work 07 par lots |
| Validation anglaise globale | Work 08 |
| Correspondance bilingue | Work 09 |
| Audit prépublication des liens interlangues déjà intégrés | Work 10 |
| Publication sans phase de mise à jour interlangue | Work 11 |
| Publication, libération et archivage | Work 11 |

Un Work ne modifie pas les données appartenant à une étape antérieure verrouillée. Toute correction structurelle postérieure passe par une migration.

## 3.3 Registre maître

Le fichier :

```text
data/registre_debat.json
```

est la source de vérité évolutive.

Les fichiers suivants sont des projections ou des livrables dérivés :

```text
graph/graphe_argumentatif.json
graph/graphe_argumentatif.md
output/*/*.wiki
aggregates/*.wiki
reports/*.txt
```

Aucune correction manuelle isolée d'un fichier dérivé ne devient normative.

## 3.4 Validation avant transition

Une étape n'est pas réputée terminée parce qu'un fichier existe.

Elle est terminée seulement si :

1. tous ses livrables obligatoires existent ;
2. les empreintes sont enregistrées ;
3. le validateur applicable a réussi ;
4. son rapport indique zéro erreur bloquante ;
5. le manifeste et le registre ont reçu le statut de sortie attendu ;
6. le fichier de transmission a été généré.

## 3.5 Pas d'écrasement silencieux

Un Work ne doit jamais :

- remplacer un fichier validé sans migration ou nouvelle version ;
- modifier un titre verrouillé ;
- réassigner un identifiant ;
- supprimer une page produite sans journal ;
- écraser une page existante sur le wiki ;
- recalculer manuellement un compteur dérivé ;
- utiliser un fichier dont l'empreinte ne correspond pas au manifeste de transmission.

---

# 4. États globaux du paquet de débat

Le manifeste du débat utilise les états suivants :

```text
initialized
graph_draft
graph_validated
graph_locked
fr_debate_validated
fr_arguments_in_progress
fr_content_complete
fr_validated
en_titles_locked
en_debate_validated
en_arguments_in_progress
en_content_complete
en_validated
bilingual_validated
interlanguage_prepared
release_ready
published
interlanguage_applied
released
archived
migration_required
blocked
```

## 4.1 Transitions principales

```text
initialized
→ graph_draft
→ graph_validated
→ graph_locked
→ fr_debate_validated
→ fr_arguments_in_progress
→ fr_content_complete
→ fr_validated
→ en_titles_locked
→ en_debate_validated
→ en_arguments_in_progress
→ en_content_complete
→ en_validated
→ bilingual_validated
→ interlanguage_prepared
→ release_ready
→ published
→ interlanguage_applied
→ released
→ archived
```

`migration_required` interrompt la progression normale jusqu'à l'application et la validation de la migration.

`blocked` indique qu'une erreur ou une collision externe empêche la transition.

---

# 5. Liste normative des Work

Le workflow comporte douze types de Work numérotés de 00 à 11.

La version 1.0 de ce workflow couvre le français puis l'anglais. Une future chaîne espagnole devra être ajoutée par versionnement explicite, sans détourner les champs ou Work anglais.

Les Work 03 et 07 sont répétés autant de fois que nécessaire pour produire les lots français et anglais.

## 5.1 Vue d'ensemble

| Numéro | Work | Nombre |
|---:|---|---:|
| 00 | Cadrage et initialisation | 1 |
| 01 | Graphe argumentatif français | 1 |
| 02 | Page Débat française | 1 |
| 03 | Arguments français — lot | Variable |
| 04 | Validation française globale | 1 |
| 05 | Registre bilingue et titres anglais | 1 |
| 06 | Page Debate anglaise | 1 |
| 07 | Arguments anglais — lot | Variable |
| 08 | Validation anglaise globale | 1 |
| 09 | Validation bilingue | 1 |
| 10 | Préparation locale des liens interlangues | 1 |
| 11 | Publication, libération et archivage | 1 |

Une migration structurelle peut créer un Work exceptionnel :

```text
[MIGRATION] <code> — <objet>
```

Ce Work n'entre pas dans la numérotation normale et doit être référencé dans `migrations.jsonl`.

---

# 6. Work 00 — Cadrage et initialisation

## 6.1 Objet

Créer le paquet vide du débat et fixer son périmètre avant toute recherche argumentative.

## 6.2 Nom de conversation

```text
[<CODE>] 00 — Cadrage et initialisation
```

Exemple :

```text
[GPA] 00 — Cadrage et initialisation
```

## 6.3 Entrées

Obligatoires :

- titre français exact du débat ;
- sources normatives dans leurs versions déclarées.

Facultatives :

- cadrage principal ;
- juridiction ;
- période ;
- sujets inclus ;
- sujets exclus ;
- débats voisins ;
- contraintes éditoriales propres au débat ;
- documents fournis par l'utilisateur.

## 6.4 Sorties

```text
manifest.json
scope.json
data/registre_debat.json
handoff/W00_to_W01.json
```

Le registre est créé à partir de `modele_registre_debat_wikidebia.json`. `scope.json` respecte `scope.schema.json` et reprend exactement le même `debate_id` et le même cadrage que l'objet `debate.scope` du registre.

## 6.5 Responsabilités

- attribuer le `debate_id` immuable ;
- attribuer le code court utilisé dans les noms de conversations ;
- fixer le titre français du débat ;
- expliciter la proposition évaluée ;
- fixer les inclusions et exclusions ;
- consigner les ambiguïtés résiduelles ;
- enregistrer les versions normatives ;
- créer l'arborescence minimale ;
- ne créer aucun argument.

## 6.6 Champs modifiables

- `schema`
- `debate.id`
- `debate.scope`
- `debate.labels.fr`
- état global du manifeste

## 6.7 Condition de réussite

- tous les fichiers obligatoires existent ;
- le JSON est valide ;
- le `debate_id` respecte la convention ;
- le cadrage est assez précis pour permettre la recherche ;
- aucune ambiguïté bloquante non signalée ne subsiste ;
- état global : `initialized`.

---

# 7. Work 01 — Graphe argumentatif français

## 7.1 Objet

Produire le graphe final, consolidé, élagué et validé, avec les titres français canoniques et affichés de tous les nœuds.

## 7.2 Nom de conversation

```text
[<CODE>] 01 — Graphe argumentatif
```

## 7.3 Entrées

```text
manifest.json
scope.json
data/registre_debat.json
handoff/W00_to_W01.json
```

Sources permanentes :

- schéma du registre ;
- prompt Work du graphe ;
- validateur du graphe.

## 7.4 Sorties

```text
data/registre_debat.json
data/lots_fr.json
graph/graphe_argumentatif.json
graph/graphe_argumentatif.md
graph/consolidation_log.json
graph/research_sources.md
graph/validation_report.txt
handoff/W01_to_W02.json
handoff/W01_to_W03.json
```

`data/lots_fr.json` est une collection de lots conforme à `batch_collection.schema.json`. Chaque objet de lot qu'elle contient est conforme à `batch_manifest.schema.json`.

## 7.5 Responsabilités

- effectuer une première recherche documentaire générale ;
- construire les nœuds, relations et occurrences ;
- effectuer séparément les passes d'omissions suivantes : débat public et littérature spécialisée ; familles disciplinaires ; acteurs et mise en œuvre ; positions intermédiaires, variantes et alternatives ; meilleures objections et contre-objections ; angles morts libres ;
- conduire une passe de saturation repartant de questions de recherche différentes ; poursuivre jusqu'à deux passes complètes consécutives sans nouvel argument important et distinct, sans dépasser six passes supplémentaires ;
- consolider les vrais doublons, tester la suppression de chaque nœud faible, élaguer les exemples et cas trop particuliers, et consigner chaque décision ;
- après élagage, effectuer une passe finale indépendante sur les arguments principaux, meilleures justifications et objections, positions intermédiaires, alternatives, acteurs, mise en œuvre et effets indirects ou de long terme ; tout ajout important relance la consolidation de la branche concernée ;
- arrêter la recherche lorsque les nouveaux résultats sont principalement des doublons, exemples ou variantes marginales, plutôt que de poursuivre indéfiniment ;
- normaliser tous les titres canoniques français ;
- fixer les titres affichés français ;
- attribuer les identifiants ;
- détecter les réutilisations ;
- déclarer la politique de profondeur ;
- créer le plan des lots français ;
- générer toutes les projections ;
- exécuter le validateur stable ;
- verrouiller le graphe.

## 7.5.1 Repères de couverture non contraignants

Sans créer de quota, le Work vise normalement environ six à dix arguments principaux par camp. Un argument principal reçoit souvent deux à cinq justifications directes et deux à cinq objections directes. Un nœud crucial développé reçoit souvent deux à quatre raisons et objections fortes. Ces repères sont abandonnés dès qu'ils produiraient des nœuds faibles, redondants ou artificiels. Les niveaux 4 ou 5 restent possibles selon la politique de profondeur verrouillée.

## 7.5.2 Contrôles logiques et documentaires

Le Work distingue explicitement principe/application, règle/exemple, cause/conséquence, constat empirique/conclusion normative, droit/morale, économie/société, existence/faisabilité d'une alternative et possibilité/coût d'une transition. Les meilleures objections contestent, selon les cas, la prémisse, le mécanisme, le lien logique, la portée, la proportionnalité, la validité empirique ou juridique, la mise en œuvre ou l'absence d'alternative moins coûteuse ou moins restrictive.

Les sources privilégient les textes et institutions officiels, la littérature scientifique, les rapports directement pertinents, les ouvrages de référence et la presse de qualité pour les positions publiques. Plusieurs positions sérieuses sont recherchées.

## 7.5.3 Contenu obligatoire des cinq livrables du graphe

`graphe_argumentatif.md` contient dans cet ordre le titre, l'arbre ASCII complet, le tableau récapitulatif recalculé, le tableau des pages réutilisées, une note concise sur les passes, une note de contrôle final et les limites résiduelles. L'arbre n'affiche que les titres, camps, libellés `Justifications`/`Objections` et crochets des réutilisations.

`validation_report.txt` emploie `VALIDATION GLOBALE : RÉUSSIE` uniquement sans erreur bloquante. `consolidation_log.json` consigne passes, ajouts, suppressions, fusions, renommages, déplacements, réutilisations, conversions en exemples, condition d'arrêt et limites. `research_sources.md` consigne titre, auteur ou institution, date disponible, lien, rôle de vérification et position réelle ou neutralité.

## 7.6 Champs modifiables

- `graph.lifecycle`
- `graph.depth_policy`
- `graph.nodes`
- `graph.edges`
- `graph.occurrences`
- `graph.derived_counts`
- titres, rubriques et mots-clés français des nœuds
- `batches` français planifiés

Les champs anglais restent non assignés.

## 7.7 Condition de réussite

- zéro erreur structurelle bloquante ;
- validation sémantique consignée ;
- tous les titres français sont `locked` ;
- état du graphe : `locked` ;
- état global : `graph_locked`;
- `structural_sha256` calculé ;
- les lots français couvrent exactement toutes les pages actives.

---

# 8. Work 02 — Page Débat française

## 8.1 Objet

Produire et valider la page Débat française à partir du graphe verrouillé.

## 8.2 Nom de conversation

```text
[<CODE>] 02 — Page Débat française
```

## 8.3 Entrées

```text
manifest.json
scope.json
data/registre_debat.json
graph/graphe_argumentatif.json
graph/research_sources.md
handoff/W01_to_W02.json
```

## 8.4 Sorties

```text
output/fr/debate/debate.wiki
data/sources.json
reports/validation_fr_debate.txt
handoff/W02_to_W04.json
```

`data/sources.json` est créé ou enrichi sans dupliquer les sources du graphe.

## 8.5 Responsabilités

- utiliser seulement les occurrences principales de profondeur 1 pour les listes ;
- reprendre exactement les titres canoniques et affichés du registre ;
- rédiger une introduction neutre, substantielle, structurée en sous-parties utiles et non transformée en liste d'arguments ;
- vérifier le contexte français, européen ou international pertinent et toutes les informations contemporaines à la date de génération ;
- vérifier l'existence et le titre exact des pages Wikipédia françaises ;
- rechercher dans chacune des neuf catégories documentaires des ressources réellement disponibles en français, sans forcer une catégorie vide ;
- classer les références selon leur position explicite réelle et conserver les sources descriptives ou contradictoires comme neutres ;
- éviter les doublons bibliographiques, sitographiques et vidéographiques ;
- produire le wikicode conforme au profil français ;
- insérer le lien interlangue `{{Lien interlangue}}` vers le titre anglais canonique verrouillé ;
- attribuer la date de génération validée.

## 8.6 Champs modifiables

- `debate.pages.fr`
- objets de sources utilisés par la page Débat
- état global vers `fr_debate_validated`

Aucun nœud, titre, relation ou occurrence ne peut être modifié.

## 8.7 Condition de réussite

- page conforme au profil ;
- arguments principaux identiques au registre ;
- introduction et sources validées ;
- `date-création` fixée ;
- absence de lien interlangue ;
- état de la page : `validated`.

---

# 9. Work 03 — Arguments français par lots

## 9.1 Objet

Produire un lot cohérent de pages Argument françaises sans modifier le graphe.

## 9.2 Noms de conversations

```text
[<CODE>] 03.FR.001 — Arguments français — <libellé du lot>
[<CODE>] 03.FR.002 — Arguments français — <libellé du lot>
```

Le numéro de conversation correspond au numéro de `batch_id`.

## 9.3 Entrées de chaque lot

```text
manifest.json
data/registre_debat.json
data/sources.json
data/lots_fr.json
graph/graphe_argumentatif.json
handoff/W01_to_W03.json
handoff/FR-A-001_input.json
```

À partir du deuxième lot, l'entrée comprend également le fichier `handoff/FR-A-<lot précédent>_output.json` et les versions actualisées du registre et de `data/sources.json`.

Le fichier d'entrée du lot contient uniquement :

- les identifiants assignés ;
- les parents et enfants nécessaires ;
- les pages réutilisées déjà produites ou attendues ;
- l'empreinte structurelle du registre ;
- les chemins de sortie autorisés.

## 9.4 Sorties de chaque lot

```text
output/fr/arguments/Axxxx.wiki
output/fr/aggregates/arguments_batch_001.wiki
data/sources.json
reports/fr_batch_001.txt
handoff/FR-A-001_output.json
```

Le registre et `lots_fr.json` sont mis à jour pour les statuts et empreintes uniquement.

## 9.5 Responsabilités

- produire exactement une page par identifiant assigné ;
- regrouper de préférence un argument principal, ses justifications et objections directes, ses descendants dépendants et les pages réutilisées non encore produites dont le lot est propriétaire ;
- reprendre exactement les relations du registre ;
- rédiger des résumés substantiels en paragraphes complets, dans un style encyclopédique grand public : thèse d’abord, mécanisme ensuite, phrases de longueur variée et définition immédiate des termes techniques nécessaires ;
- utiliser les fourchettes de longueur indicatives du profil comme signal de qualité, sans remplissage artificiel ;
- appliquer le profil scientifique resserré ;
- rechercher des références ciblées, privilégier les sources originales et vérifier leur correspondance exacte avec le résumé ;
- attribuer rubriques et mots-clés cohérents avec le registre ;
- omettre les paramètres vides ;
- insérer le lien interlangue `{{Lien interlangue}}` vers le titre anglais canonique verrouillé ;
- exécuter la validation du lot ;
- enregistrer les empreintes individuelles et agrégées ;
- rendre dans le rapport de lot le nombre de pages, les identifiants, les réutilisations, les dépendances et les difficultés de normalisation susceptibles d'affecter le sens.

## 9.6 Interdictions

Le Work de lot ne peut pas :

- créer un nœud ;
- supprimer un nœud ;
- fusionner des nœuds ;
- changer une relation ;
- renommer une page ;
- produire une page appartenant à un autre lot ;
- produire deux fois une page réutilisée ;
- modifier la date de création d'une page déjà validée.

## 9.7 Condition de réussite d'un lot

- tous les identifiants assignés possèdent une page ;
- aucune page étrangère au lot n'a été créée ;
- toutes les relations sortantes correspondent au registre ;
- zéro paramètre vide ;
- zéro lien cassé interne au paquet ;
- les sources mentionnées sont enregistrées ;
- rapport de lot réussi ;
- statut du lot : `validated`.

Quand tous les lots français sont validés :

```text
état global = fr_content_complete
```

---

# 10. Work 04 — Validation française globale

## 10.1 Objet

Valider l'ensemble de la version française avant toute fixation des titres anglais.

## 10.2 Nom de conversation

```text
[<CODE>] 04 — Validation française globale
```

## 10.3 Entrées

```text
manifest.json
scope.json
data/registre_debat.json
data/sources.json
data/lots_fr.json
graph/graphe_argumentatif.json
output/fr/debate/debate.wiki
output/fr/arguments/*.wiki
reports/fr_batch_*.txt
handoff/W02_to_W04.json
handoff/FR-A-*_output.json
```

## 10.4 Sorties

```text
reports/validation_fr.txt
reports/collision_report_fr.json
handoff/W04_to_W05.json
```

Le validateur peut régénérer les agrégats français.

## 10.5 Contrôles obligatoires

### Structure

- chaque identifiant actif possède exactement une page française ;
- aucun identifiant retiré ne possède de page ;
- aucun fichier n'est dupliqué ;
- chaque titre externe correspond au registre ;
- tous les paramètres sont autorisés ;
- tous les paramètres obligatoires sont présents ;
- aucun paramètre facultatif vide n'est présent.

### Relations

- les justifications et objections sont exhaustives et exactes ;
- aucun lien ne pointe vers un titre non canonique ;
- les pages réutilisées restent uniques ;
- aucune autojustification ni auto-objection.

### Contenu

- résumés substantiels et autonomes ;
- absence de métadiscours interdit ;
- niveau de développement proportionné à la complexité ;
- références réellement utilisées ;
- dates et lieux rédigés en français ;
- rubriques et mots-clés cohérents ;
- traitement équitable des camps.

### Collision wiki

- vérification prudente des titres français existants ;
- décision `create`, `reuse_existing`, `rename_local` ou `manual_review` ;
- aucun écrasement.

## 10.6 Corrections

Les corrections rédactionnelles locales sont autorisées.

Toute correction modifiant :

- un titre verrouillé ;
- un nœud ;
- une relation ;
- une occurrence ;
- le plan des lots ;

déclenche `migration_required`.

## 10.7 Condition de réussite

- toutes les pages françaises sont validées ;
- aucune collision non résolue ;
- aucune migration en attente ;
- état global : `fr_validated`.

---

# 11. Work 05 — Registre bilingue et titres anglais

## 11.1 Objet

Fixer les titres et métadonnées anglaises après validation complète du français, sans rédiger encore les pages anglaises.

## 11.2 Nom de conversation

```text
[<CODE>] 05 — Registre bilingue et titres anglais
```

## 11.3 Entrées

```text
manifest.json
scope.json
data/registre_debat.json
data/lots_fr.json
reports/validation_fr.txt
handoff/W04_to_W05.json
```

## 11.4 Sorties

```text
data/registre_debat.json
data/lots_en.json
reports/validation_titles_en.txt
handoff/W05_to_W06.json
handoff/W05_to_W07.json
```

`data/lots_en.json` est une collection de lots conforme à `batch_collection.schema.json`.

## 11.5 Responsabilités

- fixer le titre canonique anglais du débat ;
- fixer les libellés anglais des camps ;
- traduire et adapter tous les titres canoniques ;
- fixer tous les titres affichés anglais ;
- traduire les rubriques selon la table officielle ;
- fixer des keywords anglais idiomatiques ;
- détecter les collisions entre titres anglais ;
- vérifier les titres déjà existants sur le wiki ;
- verrouiller les titres anglais ;
- créer les lots anglais avec les mêmes identifiants que les lots français, sauf regroupement purement opérationnel motivé.

## 11.6 Interdictions

- aucune modification du raisonnement français ;
- aucune modification des relations ;
- aucune rédaction complète des pages ;
- aucun ajout de lien interlangue aux pages françaises.

## 11.7 Condition de réussite

- chaque identifiant actif possède un titre anglais unique ;
- chaque titre anglais représente le même nœud logique ;
- aucune collision non résolue ;
- tous les titres anglais sont `locked` ;
- état global : `en_titles_locked`.

---

# 12. Work 06 — Page Debate anglaise

## 12.1 Objet

Créer une page Debate anglaise autonome, adaptée au contexte anglophone ou international.

## 12.2 Nom de conversation

```text
[<CODE>] 06 — English Debate page
```

## 12.3 Entrées

```text
manifest.json
scope.json
data/registre_debat.json
data/sources.json
graph/graphe_argumentatif.json
reports/validation_fr.txt
reports/validation_titles_en.txt
handoff/W05_to_W06.json
```

## 12.4 Sorties

```text
output/en/debate/debate.wiki
data/sources.json
reports/validation_en_debate.txt
handoff/W06_to_W08.json
```

## 12.5 Responsabilités

- reprendre exactement les arguments principaux anglais verrouillés ;
- adapter l'introduction au contexte anglophone ou international ;
- vérifier les faits contemporains et appliquer les mêmes précautions épistémiques que dans la page française ;
- vérifier l'existence et le titre exact des pages Wikipedia anglaises ;
- rechercher des références réellement disponibles en anglais, plutôt que de reprendre des références françaises par défaut ;
- appliquer le profil documentaire large de la page Debate ;
- utiliser `progress=Constructed debate` ;
- utiliser `debate-warnings=Debate generated by AI` ;
- ne jamais insérer de lien interlangue ;
- fixer `creation-date`.

## 12.6 Condition de réussite

- page conforme au profil anglais ;
- même structure argumentative principale que la page française ;
- documentation anglaise vérifiée ;
- état global : `en_debate_validated`.

---

# 13. Work 07 — Arguments anglais par lots

## 13.1 Objet

Produire les pages Argument anglaises correspondant exactement aux identifiants français validés.

## 13.2 Noms de conversations

```text
[<CODE>] 07.EN.001 — English arguments — <batch label>
[<CODE>] 07.EN.002 — English arguments — <batch label>
```

## 13.3 Entrées

```text
manifest.json
data/registre_debat.json
data/sources.json
data/lots_en.json
graph/graphe_argumentatif.json
output/fr/arguments/<identifiants du lot>.wiki
reports/validation_fr.txt
handoff/W05_to_W07.json
handoff/EN-A-001_input.json
```

À partir du deuxième lot, l'entrée comprend également le handoff de sortie du lot anglais précédent et les versions actualisées du registre et de `data/sources.json`.

## 13.4 Sorties

```text
output/en/arguments/Axxxx.wiki
output/en/aggregates/arguments_batch_001.wiki
data/sources.json
reports/en_batch_001.txt
handoff/EN-A-001_output.json
```

## 13.5 Responsabilités

- produire les mêmes identifiants et les mêmes relations ;
- rédiger des résumés anglais idiomatiques en paragraphes complets, avec le même raisonnement et le même style encyclopédique grand public : thèse d’abord, rythme lisible et définition des termes techniques nécessaires ;
- maintenir un niveau de développement comparable et ne pas produire une version plus courte ou plus schématique ;
- adapter les exemples et références lorsque nécessaire, en privilégiant les sources originales et anglaises pertinentes ;
- appliquer le profil scientifique resserré ;
- respecter les dates et lieux anglais ;
- ne jamais générer d'interlangue ;
- valider chaque lot.

## 13.6 Condition de réussite

Identique au français, avec en plus :

- même ensemble d'identifiants ;
- même graphe logique ;
- titres anglais verrouillés utilisés à l'identique ;
- statut du lot anglais : `validated`.

Quand tous les lots sont validés :

```text
état global = en_content_complete
```

---

# 14. Work 08 — Validation anglaise globale

## 14.1 Objet

Valider la cohérence interne et la qualité de toutes les pages anglaises.

## 14.2 Nom de conversation

```text
[<CODE>] 08 — English global validation
```

## 14.3 Entrées

```text
manifest.json
data/registre_debat.json
data/sources.json
data/lots_en.json
output/en/debate/debate.wiki
output/en/arguments/*.wiki
reports/en_batch_*.txt
handoff/W06_to_W08.json
handoff/EN-A-*_output.json
```

## 14.4 Sorties

```text
reports/validation_en.txt
reports/collision_report_en.json
handoff/W08_to_W09.json
```

## 14.5 Contrôles

- complétude des pages ;
- paramètres et structures anglaises ;
- absence d'interlangue ;
- cohérence des titres et relations ;
- qualité idiomatique ;
- niveau de développement comparable ;
- références vérifiées ;
- dates et lieux anglais ;
- collisions wiki anglaises ;
- absence de traduction mécanique du contexte français.

## 14.6 Condition de réussite

- toutes les pages anglaises validées ;
- collisions résolues ;
- aucune migration en attente ;
- état global : `en_validated`.

---

# 15. Work 09 — Validation bilingue

## 15.1 Objet

Vérifier l'identité conceptuelle et structurelle entre les deux langues.

## 15.2 Nom de conversation

```text
[<CODE>] 09 — Validation bilingue
```

## 15.3 Entrées

```text
manifest.json
data/registre_debat.json
graph/graphe_argumentatif.json
output/fr/debate/debate.wiki
output/fr/arguments/*.wiki
output/en/debate/debate.wiki
output/en/arguments/*.wiki
reports/validation_fr.txt
reports/validation_en.txt
handoff/W08_to_W09.json
```

## 15.4 Sorties

```text
reports/validation_bilingual.txt
patches/interlanguage_fr.json
handoff/W09_to_W10.json
```

Le patch respecte `interlanguage_patch.schema.json`.

## 15.5 Contrôles obligatoires

- une page française et une page anglaise par identifiant ;
- titres canoniques distincts mais conceptuellement équivalents ;
- mêmes relations par identifiants ;
- mêmes réutilisations ;
- mêmes arguments principaux ;
- rubriques et sections correspondantes ;
- absence de collision ;
- aucune page anglaise avec interlangue ;
- cible interlangue française issue du titre canonique anglais ;
- aucune cible construite depuis un titre affiché.

## 15.6 Condition de réussite

- zéro divergence structurelle ;
- divergences éditoriales non structurelles documentées ;
- liens interlangues canoniques complets et déterministes ;
- état global : `bilingual_validated`.

---

# 16. Work 10 — Audit des liens interlangues intégrés

## 16.1 Objet

Contrôler que tous les fichiers français canoniques contiennent déjà leur lien interlangue définitif, que toutes les cibles proviennent des titres anglais verrouillés et qu'aucune page anglaise ne contient de lien interlangue.

## 16.2 Nom de conversation

```text
[<CODE>] 10 — Audit interlangue intégré
```

## 16.3 Entrées

```text
manifest.json
data/registre_debat.json
output/fr/debate/debate.wiki
output/fr/arguments/*.wiki
output/en/debate/debate.wiki
output/en/arguments/*.wiki
reports/validation_bilingual.txt
handoff/W09_to_W10.json
```

## 16.4 Sorties

```text
reports/validation_interlanguage.txt
logs/interlanguage_audit.jsonl
handoff/W10_to_W11.json
```

Aucun fichier `staging/interlanguage/` et aucun patch `patches/interlanguage_fr*` ne sont produits pour un paquet 1.2.0.

## 16.5 Responsabilités

- vérifier exactement un `|interlangue={{Lien interlangue...}}` dans chaque page française ;
- vérifier que `langue=en` et que `page=` reproduit le titre canonique anglais du même identifiant ;
- accepter que la cible anglaise ne soit pas encore publiée, dès lors qu'elle est verrouillée et planifiée ;
- vérifier l'absence de lien interlangue dans toutes les pages anglaises ;
- vérifier que `date-création` n'a pas été modifiée ;
- vérifier l'absence de `<references />` et l'usage de `topic` / `complete-topic` dans la page Debate anglaise ;
- ne pas modifier les fichiers ;
- ne pas se connecter au wiki.

## 16.6 Condition de réussite

- un seul lien conforme par page française canonique ;
- aucune cible construite depuis un titre affiché ;
- aucun lien dans les pages anglaises ;
- aucun fichier de staging ou patch interlangue requis ;
- rapport réussi ;
- état global : `interlanguage_validated`, puis `release_ready`.

---

# 17. Work 11 — Publication, libération et archivage

## 17.1 Objet

Contrôler le paquet final, publier les pages françaises déjà complètes puis les pages anglaises, et clôturer le débat sans modification interlangue distincte.

## 17.2 Nom de conversation

```text
[<CODE>] 11 — Publication et archivage
```

## 17.3 Entrées

Tout le paquet validé, notamment :

```text
manifest.json
data/registre_debat.json
reports/validation_fr.txt
reports/validation_en.txt
reports/validation_bilingual.txt
reports/validation_interlanguage.txt
output/fr/debate/debate.wiki
output/fr/arguments/*.wiki
output/en/debate/debate.wiki
output/en/arguments/*.wiki
logs/interlanguage_audit.jsonl
handoff/W10_to_W11.json
```

## 17.4 Sorties

```text
logs/import_fr.jsonl
logs/import_en.jsonl
reports/release_report.txt
release_manifest.json
archive_checklist.txt
<debate_id>_release.zip
<debate_id>_release_receipt.json
```

`release_manifest.json` respecte `release_manifest.schema.json`. Sa liste `files` exclut le manifeste lui-même ; l'empreinte de l'archive est conservée dans un reçu externe.

## 17.5 Ordre de publication obligatoire

La page anglaise peut être absente lors de la création française, mais toutes les cibles anglaises doivent être verrouillées et incluses dans le plan signé :

1. vérifier localement tous les liens interlangues français intégrés ;
2. vérifier à distance tous les titres français ;
3. importer les pages Argument françaises depuis `output/fr/arguments/` ;
4. importer la page Débat française depuis `output/fr/debate/debate.wiki` ;
5. effectuer la vérification post-import française ;
6. vérifier à distance tous les titres anglais ;
7. importer les pages Argument anglaises ;
8. importer la page Debate anglaise ;
9. effectuer la vérification post-import anglaise ;
10. vérifier que chaque cible anglaise est `created` ou `equivalent_existing` ;
11. produire le manifeste de libération sans réécrire les pages françaises ;
12. effectuer la vérification finale des liens et des révisions.

## 17.6 Règles d'import

- simulation obligatoire avant écriture ;
- plan global signé couvrant les deux langues ;
- création exclusive pour les nouvelles pages ;
- aucun écrasement par défaut ;
- aucune opération `parameter_update` visant `interlangue` ;
- comparaison locale et distante ;
- reprise fondée sur le titre et le SHA-256 du contenu ;
- journalisation de chaque opération ;
- enregistrement et relecture de la révision exacte ;
- collisions soumises à décision éditoriale ;
- arrêt si une cible anglaise planifiée disparaît ou diverge avant l'écriture française.

## 17.7 Condition de réussite

- toutes les pages françaises et anglaises créées ou reconnues équivalentes ;
- liens interlangues français vérifiés sans seconde écriture ;
- zéro collision non résolue ;
- journaux et révisions cohérents ;
- manifeste de libération et archive produits ;
- état global : `release_ready`, puis archivage après publication vérifiée.

# 18. Production par lots

## 18.0 Séquencement

Dans la version 1.0, les lots d'une même langue sont exécutés séquentiellement, jamais en parallèle. Chaque lot reçoit le registre, le registre documentaire et le handoff de sortie du lot précédent. Cette règle évite les collisions d'identifiants de sources, les pertes de mise à jour et les divergences d'empreintes.

Le premier lot français part du handoff du Work 01 ; le premier lot anglais part du handoff du Work 05. Une future exécution parallèle exigerait un protocole explicite de deltas et de fusion versionné.

## 18.1 Taille

Un lot contient normalement entre 10 et 25 pages distinctes.

Cette taille est indicative. La cohérence intellectuelle et la qualité priment.

## 18.2 Critère principal de regroupement

Ordre de préférence :

1. un argument principal et son sous-graphe ;
2. plusieurs sous-branches étroitement liées ;
3. un groupe de pages réutilisées et leurs principaux contextes ;
4. un découpage quantitatif seulement si les critères précédents ne suffisent pas.

## 18.3 Pages réutilisées

Chaque page est assignée à exactement un lot propriétaire par langue.

Les autres lots :

- peuvent la lire ;
- peuvent créer des liens vers elle ;
- ne peuvent pas la régénérer ;
- enregistrent sa dépendance dans leur manifeste.

## 18.4 Lot trop volumineux

Un sous-graphe supérieur à environ 25 pages peut être divisé, à condition de :

- conserver un lot propriétaire pour chaque page ;
- enregistrer les dépendances ;
- fournir aux lots secondaires le contexte nécessaire ;
- ne pas dupliquer le contenu.

## 18.5 Validation par lot

Chaque lot réalise :

- une validation syntaxique ;
- une validation des paramètres ;
- une validation des relations ;
- une validation des références ;
- un contrôle des titres ;
- un rapport de couverture indiquant le nombre de pages, les identifiants, les réutilisations, dépendances et difficultés de normalisation ;
- un calcul d'empreintes.

La validation globale ne remplace pas la validation de lot.

---

# 19. Transmission entre Work

## 19.1 Principe

Chaque Work reçoit un fichier de transmission entrant et produit un fichier de transmission sortant.

Format de référence :

```text
handoff/<origine>_to_<destination>.json
```

ou, pour les lots :

```text
handoff/FR-A-001_input.json
handoff/FR-A-001_output.json
```

## 19.2 Contenu minimal

Le fichier contient :

- identifiant du débat ;
- étape d'origine ;
- étape de destination ;
- état global attendu ;
- versions normatives ;
- fichiers requis ;
- SHA-256 de chaque fichier ;
- champs verrouillés ;
- chemins de sortie autorisés ;
- validations préalables ;
- date de création ;
- résultat de l'étape d'origine.

## 19.3 Règles du Work récepteur

Le Work récepteur doit :

1. vérifier le `debate_id` ;
2. vérifier les versions ;
3. vérifier les empreintes ;
4. vérifier l'état global ;
5. vérifier les validations préalables ;
6. travailler uniquement dans les chemins autorisés ;
7. ne pas modifier les champs verrouillés ;
8. produire un fichier de sortie déclarant toutes les modifications.

Une empreinte incorrecte rend le Work `blocked`. Il ne doit pas deviner quel fichier est le plus récent.

## 19.4 Bundle d'entrée

Pour simplifier l'usage dans ChatGPT Work, les fichiers d'entrée peuvent être regroupés dans :

```text
work_inputs/<work_id>_input.zip
```

Le ZIP contient :

- le handoff ;
- uniquement les fichiers nécessaires ;
- un inventaire ;
- les empreintes.

Les sources normatives permanentes ne sont pas dupliquées dans chaque ZIP si elles sont disponibles et versionnées dans les sources du projet.

---

# 20. Conventions de nommage

## 20.1 Code court du débat

Le code court est :

- unique parmi les débats actifs ;
- composé de 2 à 8 caractères majuscules et chiffres ;
- stable pendant toute la production.

Exemples :

```text
GPA
PARA
RSA
```

## 20.2 Conversations

```text
[CODE] 00 — Cadrage et initialisation
[CODE] 01 — Graphe argumentatif
[CODE] 02 — Page Débat française
[CODE] 03.FR.001 — Arguments français — <libellé>
[CODE] 04 — Validation française globale
[CODE] 05 — Registre bilingue et titres anglais
[CODE] 06 — English Debate page
[CODE] 07.EN.001 — English arguments — <label>
[CODE] 08 — English global validation
[CODE] 09 — Validation bilingue
[CODE] 10 — Liens interlangues
[CODE] 11 — Publication et archivage
```

## 20.3 Fichiers de pages

```text
output/fr/debate/debate.wiki
output/en/debate/debate.wiki
output/fr/arguments/A0001.wiki
output/en/arguments/A0001.wiki
```

Les noms de fichiers utilisent les identifiants, jamais les titres textuels.

## 20.4 Agrégats

```text
arguments_batch_001.wiki
arguments_batch_002.wiki
```

Les agrégats sont régénérés depuis les fichiers individuels et ne sont jamais édités manuellement. Chaque page y est précédée du séparateur exact :

```text
===== PAGE : Titre canonique exact =====
```

Le contenu commence à la ligne suivante. Deux pages successives sont séparées par une ligne vide. Le titre du séparateur doit être strictement identique au titre canonique du registre.

Les objets décrivant individuellement les pages dans `manifest.json` respectent `page_manifest.schema.json`. Des projections autonomes peuvent être générées pour les outils, mais elles sont dérivées et ne constituent pas une source de vérité supplémentaire.

---

# 21. Migrations après verrouillage

## 21.1 Déclencheurs

Une migration est obligatoire pour :

- ajouter ou retirer un nœud ;
- fusionner ou scinder un nœud ;
- modifier une relation ;
- modifier une occurrence ;
- renommer un titre verrouillé ;
- changer un identifiant ;
- modifier un titre anglais après génération des pages anglaises.

## 21.2 Procédure

1. état global vers `migration_required` ;
2. création d'un objet migration ;
3. inventaire des fichiers et lots affectés ;
4. modification du registre ;
5. régénération des projections ;
6. invalidation des pages devenues obsolètes ;
7. régénération des pages affectées ;
8. relance des validations concernées ;
9. nouvelle empreinte structurelle ;
10. reprise du workflow à l'étape appropriée.

## 21.3 Pas de correction cachée

Une correction rédactionnelle sans effet structurel peut être locale.

Dès qu'une correction modifie l'identité ou les relations d'une page, elle est structurelle et doit être migrée.

---

# 22. Gestion des échecs

## 22.1 Erreur bloquante

Une erreur est bloquante lorsqu'elle touche :

- le schéma ;
- un identifiant ;
- une relation ;
- un titre canonique verrouillé ;
- une page manquante ;
- une duplication ;
- une collision non résolue ;
- une référence inventée ou fausse ;
- un lien interlangue incorrect ;
- une divergence bilingue structurelle ;
- un paramètre obligatoire absent ;
- un paramètre interdit.

## 22.2 Sortie d'un Work en échec

Même en échec, le Work doit produire :

```text
reports/<work_id>_failure.txt
handoff/<work_id>_blocked.json
```

Il ne doit pas modifier le statut vers l'étape suivante.

## 22.3 Reprise

La reprise utilise :

- le dernier registre valide ;
- le handoff réussi le plus récent ;
- les empreintes ;
- les pages déjà validées ;
- les rapports d'échec.

Aucune étape complète n'est recommencée lorsqu'une correction ciblée suffit.

---

# 23. Réduction des erreurs de contexte et de la perte de qualité

## 23.1 Prompts spécialisés

Chaque prompt ne traite qu'une tâche :

- recherche et structure ;
- rédaction d'une page Débat ;
- rédaction d'un lot ;
- validation ;
- adaptation anglaise ;
- interlangue ;
- publication.

## 23.2 Entrées minimales

Un Work reçoit uniquement les fichiers nécessaires. Un ancien débat ou un ancien lot non pertinent n'est pas attaché.

## 23.3 Titres et relations verrouillés

Le rédacteur d'une page ne choisit pas son titre ni ses relations. Il développe un nœud déjà identifié.

## 23.4 Lots limités

La production par lots empêche la dégradation des dernières pages d'une très longue exécution.

## 23.5 Validations successives

Les contrôles ont lieu :

- à la sortie du graphe ;
- à la sortie de chaque lot ;
- globalement en français ;
- à la sortie de chaque lot anglais ;
- globalement en anglais ;
- bilinguellement ;
- après interlangue ;
- après import.

## 23.6 Sources versionnées

Les Work déclarent les versions des normes qu'ils appliquent. Une modification des normes ne change pas silencieusement un débat en cours.

## 23.7 Aucun recours au contexte conversationnel comme donnée

Les choix structurants doivent figurer dans un fichier. Une conversation peut expliquer une décision, mais le paquet doit la consigner avant le Work suivant.

---

# 24. Conditions de clôture d'un débat

Un débat peut être clôturé seulement si :

1. le graphe est verrouillé ;
2. toutes les pages françaises sont validées ;
3. toutes les pages anglaises sont validées ;
4. la validation bilingue est réussie ;
5. les collisions sont résolues ;
6. les liens interlangues applicables sont insérés et vérifiés ;
7. les journaux d'import sont complets ;
8. le paquet final est autonome ;
9. l'archive ZIP est vérifiée ;
10. le rapport de libération indique zéro erreur bloquante.

---

# 25. Livrable final minimal d'un débat

```text
<debate_id>_release/
├── manifest.json
├── release_manifest.json
├── scope.json
├── data/
├── graph/
├── output/
├── patches/
├── reports/
├── logs/
├── release_report.txt
└── archive_checklist.txt
```

Le reçu externe `<debate_id>_release_receipt.json` est conservé à côté du ZIP, hors de celui-ci, afin d'éviter toute auto-référence cryptographique. Le ZIP est un instantané immuable à l'état `released`. Le passage administratif à `archived` est enregistré dans le reçu externe et, si nécessaire, dans la copie de travail postérieure, sans reconstruire silencieusement le ZIP.

Le paquet final doit permettre :

- de comprendre le cadrage ;
- de reconstruire le graphe ;
- de vérifier toutes les pages ;
- de régénérer les agrégats ;
- de reprendre un import interrompu ;
- d'effectuer une migration ultérieure ;
- de prouver les versions normatives utilisées.

---

# 26. Étapes suivantes de construction du système

Après validation de ce workflow, les travaux suivants sont réalisés dans cet ordre :

1. créer les schémas JSON exécutables ;
2. construire le validateur stable ;
3. rédiger les prompts Work 00 à 11 ;
4. produire les messages courts de lancement ;
5. adapter le dossier Pywikibot ;
6. tester le système sur un débat pilote ;
7. corriger les normes et passer en version 1.1 ou 2.0 si nécessaire.

---

# Addendum intégré 1.1.0 — workflow correctif

Le cycle autorisé est `release_ready → corrective_in_progress → corrective_blocked/corrective_in_progress → release_ready`. Le Work porte le type `corrective_prepublication`. De nouveaux instantanés et handoffs correctifs sont créés sans modifier les handoffs historiques. Le retour à `release_ready` exige une validation complète, une revue humaine enregistrée, zéro avertissement non résolu et la preuve de l’absence d’écriture distante.

La préparation W11 est séparée de W10.R1. Elle ne peut pas être exécutée pendant la reprise et doit vérifier la compatibilité distante des modèles avant toute écriture.
# Addendum intégré 1.1.4 — workflow historique

Chaque reprise corrective produit un handoff final nouveau et un audit de non-régression. Une seule norme consolidée demeure active à la racine. La livraison complète inclut le kit W11 non exécuté. W11 importe les arguments français avant le débat français, puis les arguments anglais avant le débat anglais ; les interlangues françaises font déjà partie des créations. Les pages existantes équivalentes sont ignorées ; toute collision bloque par défaut. Les écritures sont relues, journalisées et reprenables par titre + SHA-256.

### Complément W11 1.2.0 — plan exact et empreintes

Les modes de test et de publication chargent obligatoirement le fichier de plan signé issu de la simulation. Ils ne reconstruisent pas un plan implicite. Le plan porte les empreintes du manifeste, du manifeste de libération et du validateur ; toute divergence bloque l’exécution. Une reprise après interruption reconnaît aussi une page française déjà égale à la version finale avec interlangue.
# Addendum 1.1.5

W11 exige un reçu de test utilisateur lié au SHA-256 exact du plan avant le mode de publication canonique.


# Addendum 1.1.5 — historique, remplacé par 1.1.7

La source normative active unique est `WIKIDEBIA_NORME_CONSOLIDEE_1.1.9.md`. Chaque titre affiché et chaque ensemble de rubriques fait l’objet d’une décision page par page ; aucun quota global ne remplace cette revue. Une rubrique ubiquitaire est admise lorsque sa pertinence est justifiée pour chaque nœud. W11 1.3.1 exige un reçu vérifiable du test utilisateur lié au plan signé avant toute publication canonique. Toute disposition antérieure incompatible est historique.


# Addendum intégré 1.1.7 — règle active

Chaque rubrique retenue est justifiée individuellement au moyen d’une structure générique ; aucune rubrique ne reçoit de traitement spécial. Les dates et chemins propres à un corpus sont déclarés par son manifeste et ne sont pas codés dans le moteur de validation. Toute disposition antérieure incompatible est historique.

# Addendum intégré 1.1.8 — contrôle rédactionnel des résumés

Après chaque lot, une relecture distincte vérifie page par page : idée principale annoncée immédiatement, absence d'enchaînement soporifique de phrases longues, vocabulaire compréhensible sans formation spécialisée, définition des termes techniques indispensables, absence de noms d'études accumulés avant l'explication et conservation exacte du nœud logique. Le rapport de revue est déclaré dans `manifest.json.editorial_controls.summary_style_review_path`.

# Addendum intégré 1.1.9 — contre-relecture de l’ouverture, des exemples et du ton

Après chaque lot bilingue, la contre-relecture éditoriale vérifie séparément, pour chaque page et chaque langue :

1. que la première phrase développe le titre par un phénomène, une prémisse, un mécanisme, une conséquence ou une distinction utile ;
2. qu’aucun exemple n’est ajouté comme simple décoration et que son caractère réel ou hypothétique est clair ;
3. que toute donnée chiffrée est soutenue par la documentation de la page, contextualisée et attestée dans le registre de revue ;
4. que le résumé expose la version forte de l’argument avec une formulation ferme lorsque cela sert la compréhension ;
5. que cette fermeté ne devient ni sarcasme, ni caricature, ni slogan, ni répétition mécanique d’une formule d’un résumé à l’autre.

Le registre déclaré dans `manifest.json.editorial_controls.summary_style_review_path` contient, pour chaque langue produite, les attestations booléennes `opening_develops_title`, `example_or_data_reviewed`, `assertive_tone_reviewed`, `no_artificial_example_or_number` et `no_polemical_overstatement`. Lorsqu’une donnée chiffrée est présente, il contient aussi `quantitative_claims_verified=true` et une `quantitative_claims_note` non vide indiquant la nature de la vérification. L’absence d’exemple ou de chiffre est admise et ne constitue jamais une anomalie en soi.


# Addendum actif 1.2.0 — séquence de production

Cet addendum remplace toute séquence incompatible ci-dessus. Le Work 01 fixe et verrouille les titres canoniques des deux langues après stabilisation du graphe. Les Work 02 et 03 créent les pages françaises avec `{{Lien interlangue}}`, même si les pages anglaises seront rédigées et créées dans les Work 06 et 07. Le Work 05 devient un audit bilingue des titres déjà verrouillés. Le Work 10 vérifie les liens présents dans les fichiers canoniques et ne produit ni patch ni staging. Le Work 11 publie les pages françaises puis anglaises en mode création uniquement ; aucune modification interlangue ultérieure n’est nécessaire. Les paquets 1.1.x conservent leur ancien workflow à titre de compatibilité historique.


# Addendum actif 1.2.1 — revue des titres et de la prose française

Avant verrouillage du graphe, contrôler que chaque titre canonique reste intelligible hors de sa branche et que tout démonstratif ou pronom possède un antécédent dans le titre lui-même. Les titres affichés sont relus dans chacun de leurs emplacements. Avant validation française et avant publication, rechercher les paires de tirets cadratins employées comme parenthèses dans les introductions et résumés et les remplacer par des parenthèses.
