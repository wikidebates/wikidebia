## 0.4.73 — 10 août 2026 — alignement des métadonnées de première publication anglaise

- ne projette plus `initialisation` vers `initialization` dans le chemin `translated_english` d’une nouvelle page ;
- ne compare plus `creation-date` anglaise à `date-création` française ;
- conserve la préservation historique d’`initialization` et de `creation-date` sur les pages anglaises préexistantes ;
- ajoute des régressions d’exécution et restaure l’attribution historique exacte de 0.4.71/0.4.72.

## 0.4.72 — 10 août 2026 — renommage des paramètres MediaWiki

- valide `sujet-développé` / `expanded-topic` et `débat-dédié` / `dedicated-debate` comme paramètres courants ;
- conserve la lecture des anciens noms pour les paquets antérieurs à 1.2.69 ;
- refuse la coexistence des anciennes et nouvelles formes dans une sortie courante.

## 0.4.71 — 10 août 2026 — familles de convergence normalisées

- accepte les reçus de convergence 1.0 et 1.1 ;
- exige pour 1.1 deux `method_family` finales distinctes ;
- conserve tous les contrôles de 0.4.70.

## 0.4.70 — 10 août 2026 — revue idiomatique et corpus réel de régressions

- accepte la revue sémantique 1.4 et le moteur de marqueurs 1.3 ;
- distingue changement idiomatique revu et dégradation formelle ;
- étend les risques lexicaux et le corpus de fixtures réelles ;
- maintient la convergence obligatoire pour les revues 1.3 et 1.4.

## 0.4.69 — 10 août 2026 — équivalence propositionnelle et convergence sémantique

- contrôle le prédicat principal des displayed-title anglais ;
- étend les signaux différentiels et le métadiscours anglais ;
- valide les preuves de champ, les concept_id et le reçu de convergence ;
- ajoute les régressions multiligne et les codes WDV-BIL-008/009, WDV-EDT-033.

## 0.4.68 — 10 août 2026 — cohérence des documents actifs

- aligne la copie normative sur 1.2.65 ;
- corrige le diagnostic utilisateur qui appelait encore `name=` le champ MediaWiki anglais alors que `name` n’est plus qu’un champ interne de registre ;
- ajoute des tests empêchant le retour des contradictions actives sur l’interlangue différée et les Citation/Quote.

## 0.4.67 — 10 août 2026 — continuité de compatibilité

- restaure `1.2.62` dans `compatible_normative_revisions` et `supported_normative_revisions` ;
- supprime la duplication accidentelle de `1.2.63` ;
- aligne le validateur sur la norme 1.2.64 et le kit 2.15.48, sans changement de logique de validation éditoriale.

## 0.4.66 — 10 août 2026 — correctif de réconciliation

- aligne la copie normative sur 1.2.63 ;
- ajoute des tests garantissant la terminologie active `established-name` / `AI-translated quote` et la cohérence des contrats fusionnés.

## 0.4.65 — 10 août 2026 — réconciliation traduction + publication

- fusionne les deux variantes 0.4.64 développées en parallèle ;
- conserve la validation différentielle FR→EN, les signaux sémantiques structurés, les registres documentaires et les contrôles de scellement ;
- intègre `nom-consacré` / `established-name`, `AI-translated quote`, l'interdiction d'`initialization` sur les nouveaux Arguments EN et les contrôles de cohérence normative de la branche GitHub ;
- combine l'attestation humaine de proposition/intelligibilité avec le contrôle différentiel sans permettre à une attestation générique d'annuler une régression FR→EN ;
- aligne les schémas et la copie normative sur 1.2.62.

Les changelogs complets des deux branches 0.4.64 sont conservés sous `branch_history/`.

## 0.4.74 — 10 août 2026 — compatibilité pilotée par schémas et capacités

- ajoute un schéma explicite `wikidebia-validator-report-1.0` aux rapports ;
- centralise les versions courantes dans `VERSIONS.json` ;
- remplace les listes manuelles de révisions compatibles par une dérivation historique informative ;
- conserve les numéros de producteur comme provenance sans les utiliser comme feature flags.

## 0.4.75 — 11 août 2026 — maintenance d’alignement graph-extract

- aucune modification des règles de validation éditoriale ;
- aligne la release sur la norme 1.2.72 et le kit 2.15.56 ;
- conserve `complete_topic` et `detailed_debate` comme clés internes historiques ;
- la régression CLI est corrigée et testée dans le kit.


## 0.4.76 — 11 août 2026 — contrats d’orchestration éditoriale

- s’aligne sur la norme 1.2.73 et le kit 2.16.0 ;
- ajoute les schémas JSON des paquets ChatGPT, de l’état d’orchestration et des réponses de convergence ;
- déclare ces schémas dans `CAPABILITIES.json` ;
- conserve l’intégralité des contrôles éditoriaux, différentiels, documentaires et de publication précédents.

## 0.4.77 — 11 août 2026 — sévérité fonctionnelle des titres avant revue

- `WDV-GRA-016` et `WDV-EDT-016` relatifs aux titres importés sont des avertissements tant que le verrou de métadonnées de la langue concernée n’existe pas ;
- ces contrôles redeviennent bloquants dès présence de `data/fr_page_metadata_lock.json` ou `data/en_page_metadata_lock.json` ;
- les collisions, cycles, auto-relations, relations/occurrences invalides et autres incohérences structurelles restent bloquantes sans assouplissement ;
- ajoute des tests positif/négatif empêchant une nouvelle confusion entre signal éditorial pré-revue et erreur structurelle.

## 0.4.78 — 11 août 2026 — maintenance d’alignement short_code

- aucune modification des contrôles de validation ;
- aligne les métadonnées de release sur la norme 1.2.75 et le kit 2.16.2 ;
- conserve intégralement la sévérité fonctionnelle pré-revue introduite en 0.4.77.
## 0.4.79 — 11 août 2026 — schéma de correction du graphe

- ajoute et catalogue `graph_correction.schema.json` pour `wikidebia-graph-correction-1.0` ;
- déclare la capacité de lecture du document de correction utilisé après rejet d’une revue de graphe ;
- ne modifie aucun contrôle éditorial ou structurel existant du corpus.

## 0.4.80 — 11 août 2026 — alignement sur les actions structurelles de revue

- aligne la copie normative sur 1.2.77 et le kit recommandé sur 2.16.4 ;
- conserve tous les contrôles structurels et éditoriaux existants ;
- permet au kit de valider prospectivement le corpus reconstruit avant l’exécution distante des actions de graphe.

## 0.4.81 — 12 août 2026 — validation différentielle des métadonnées historiques

- aligne le validateur sur la norme 1.2.78 ;
- n’émet plus `WDV-EDT-021` pour le seul caractère non propositionnel d’un `displayed-title` appartenant à une page `preexisting` ;
- n’applique plus le contrôle de quantité 2–4 aux keywords d’une page Argument `preexisting` ;
- maintient les contrôles de forme flagrante, de vocabulaire, de capitalisation, de cohérence et tous les contrôles stricts pour les pages `new` ;
- ajoute des régressions positives/négatives sur `new` vs `preexisting`.

## 0.4.82 — 12 août 2026 — tournures impersonnelles françaises

- corrige `contextual_title_issues` afin que `Il ne faut…` ne soit plus interprété comme un pronom anaphorique ;
- conserve la détection des vrais référents contextuels initiaux ;
- ajoute un test positif pour `Il faut…` / `Il ne faut…` et un test négatif pour `Il réduit…` ;
- aucune modification de la norme éditoriale 1.2.78.

## 0.4.83 — 12 août 2026 — contrôle des résumés individualisés de reprise

- aligne le validateur sur la norme 1.2.79 et le kit 2.16.12 ;
- accepte le contrat additif `edit_summary_contract=page_specific_v1` dans les plans `wikidebia-remote-update-plan-1.0` ;
- ajoute `WDV-RMT-008` pour bloquer une mutation sans politique/résumé individualisés ou portant encore le résumé générique `Corrections` ;
- conserve la lecture des plans historiques dépourvus de ce contrat ;
- ne modifie aucun contrôle éditorial de contenu.

## 0.4.84 — 12 août 2026 — alignement checkpoint français 1.2.80

- aligne la copie normative sur la publication française automatique après `fr_content_review` ;
- conserve `WDV-RMT-008` et tous les contrôles de résumés individualisés ;
- reconnaît le checkpoint français comme corpus `translation_status.en=deferred` contrôlé avant reprise distante ;
- ne modifie aucun contrôle sémantique FR→EN ni aucune règle de traduction.

## 0.4.85 — 12 août 2026 — alignement sur les deux checkpoints français

- aligne la copie normative sur 1.2.81 et le kit recommandé sur 2.16.14 ;
- conserve `WDV-RMT-008` et tous les contrôles existants de plans/résumés individualisés ;
- reconnaît les checkpoints français graphe/titres et contenu/classification comme deux usages successifs du même contrat de corpus/plan ;
- aucune règle sémantique ou bilingue n’est assouplie.

## 0.4.87 — 12 août 2026 — verrouillage des textes historiques français

- s’aligne sur la norme 1.2.83 et le kit 2.16.16 ;
- ajoute `WDV-EDT-034` pour détecter toute divergence entre les empreintes historiques scellées et l’introduction/résumé rendu ;
- traite `historical_existing` et `historical_absent` comme états de préservation, sans imposer rétroactivement les règles de création ;
- couvre par tests la conservation exacte, la réécriture interdite du résumé, la réécriture interdite de l’introduction et l’acceptation d’une introduction historique ne satisfaisant pas les contraintes de nouvelle création.
- accepte `translated_historical_source` pour la traduction d’un résumé français historique protégé, sans appliquer les exigences de création à la source préexistante.

## 0.4.88 — 12 août 2026 — validation du consentement propriétaire historique

- aligne `WDV-EDT-034` sur `preserved` / `authorized_change` ;
- vérifie le reçu local de workflow, son scellement et sa portée exacte ;
- compare le rendu à l’empreinte historique pour `preserved` et à l’empreinte finale autorisée pour `authorized_change` ;
- refuse une fausse autorisation, un delta hors portée et une création historique absente non autorisée ;
- conserve la validation différentielle de la traduction à partir de la version française finale autorisée.
