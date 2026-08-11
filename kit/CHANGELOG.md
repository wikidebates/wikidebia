## 2.15.54 — 10 août 2026 — alignement des métadonnées de première publication anglaise

- aligne le validateur courant sur le contrat déjà actif : aucune projection `initialisation` → `initialization` pour une nouvelle traduction anglaise ;
- conserve `creation-date` anglaise indépendante de `date-création` française et sous responsabilité du jour réel de première publication distante ;
- préserve les métadonnées historiques des pages anglaises préexistantes ;
- ajoute des tests d’exécution croisés et restaure l’attribution historique exacte des versions 2.15.52 et 2.15.53.

## 2.15.53 — 10 août 2026 — renommage des paramètres MediaWiki

- émet `sujet-développé` / `expanded-topic` et `débat-dédié` / `dedicated-debate` dans les sorties courantes ;
- conserve la lecture des anciens noms pour les corpus historiques et normalise les reprises sans modifier les valeurs ;
- ajoute les tests de migration, de reprise et de non-coexistence des anciens/nouveaux noms.

## 2.15.52 — 10 août 2026 — durcissement final des preuves

- normalise les familles de méthodes des passes de convergence ;
- ajoute la régression explicite `established-name=` → keyword ;
- teste le parsing multiligne jusque dans `wikidebia_publish.py` ;
- conserve tous les comportements éditoriaux de 2.15.51.

## 2.15.51 — 10 août 2026 — régressions réelles et changements idiomatiques revus

- changement de forme du displayed-title autorisé seulement avec revue de l’acte de langage ;
- corpus versionné de régressions FR→EN réelles, mauvaises/corrigées ;
- catalogue sémantique aligné avec le validateur ;
- preuves source/cible obligatoires pour les risques ;
- preuves par champ Debate propagées dans les verrous.

## 2.15.50 — 10 août 2026 — preuve sémantique et convergence finale

- enrichit translation_review avec empreintes, preuves et risques ;
- ajoute la commande de convergence à deux passes distinctes ;
- bloque l'application sans reçu convergé et propage sa preuve jusqu'à la release ;
- ajoute les concept_id déterministes et les régressions de parsing multiligne.

## 2.15.49 — 10 août 2026 — cohérence documentaire croisée

- aligne les métadonnées sur la norme 1.2.65 et le validateur 0.4.68 ;
- ajoute un test croisé vérifiant que le guide actif des Normes emploie `nom-consacré=` / `established-name=` ;
- ajoute le regression gate `active_document_contract_consistency`.

## 2.15.48 — 10 août 2026 — tests critiques autonomes

- rend `test_wikidebia_remote_update.py` autonome en ajoutant explicitement `scripts/` à son chemin d’import ;
- applique la même correction à `test_reference_note_punctuation_1244.py` ;
- ajoute deux tests de régression qui relancent ces modules dans des processus pytest réellement isolés ;
- aligne les métadonnées sur la norme 1.2.64 et le validateur 0.4.67.

## 2.15.47 — 10 août 2026 — correctif de réconciliation

- restaure dans `KIT_MANIFEST.json` les scopes, règles de sécurité, features, quality gates et regression gates de la branche publication ;
- aligne les guides actifs sur `nom-consacré` / `established-name` et `AI-translated quote` ;
- ajoute des tests ciblés empêchant la perte déclarative d’une capacité de branche lors d’une future fusion.

## 2.15.46 — 10 août 2026 — réconciliation traduction + publication

- fusionne la lignée traduction/validation 2.15.38 avec la lignée de publication GitHub 2.15.45 (`8b46816`) ;
- conserve la validation différentielle, le moteur de marqueurs sémantiques, la revue de portée des appellations consacrées, le registre documentaire, la complétude des `Quote`, la validation multicouche et le scellement d’archive de la lignée traduction ;
- conserve les résumés de publication FR→EN, les balises `translated-fr`, le rattrapage de balises, la reprise interlangue, la relecture distante bornée, `nom-consacré` / `established-name`, la politique `initialization` et la date réelle de création anglaise de la lignée GitHub ;
- archive les historiques de branches lorsque les mêmes numéros de version avaient été réutilisés avec des changements différents ;
- aligne le kit sur la norme 1.2.62 et le validateur 0.4.65.

L’historique exact des deux branches antérieures est conservé sous `branch_history/`.

## 2.15.55 — 10 août 2026 — workflows version-agnostiques et release canonique

- centralise les versions courantes dans `VERSIONS.json` via `wikidebia_release_info.py` ;
- remplace les égalités exactes kit/validateur des workflows par des contrats de schéma/capacité ;
- normalise à l’entrée les labels historiques des plans et paramètres MediaWiki ;
- fait de la release complète unique le format standard pour upgrade, audit, conservation et handoff.

## 2.15.56 — 11 août 2026 — correction graph-extract dedicated-debate

- corrige le `Namespace` de `graph-extract` : `args.follow_local_relations_at_dedicated_debate` est désormais utilisé de bout en bout ;
- conserve `--follow-local-relations-at-detailed-debate` comme alias d’entrée historique ;
- ne renomme pas les clés internes `complete_topic` et `detailed_debate`, conformément au contrat 1.2.69 ;
- ajoute des tests de régression sur `main()` et sur les deux noms d’option ;
- aucune modification des formats de corpus, des règles éditoriales ou des contrats de publication.


## 2.16.0 — 11 août 2026 — orchestration ergonomique des revues ChatGPT

- ajoute `workflow`, `review-import` et `workflow-status` au lanceur principal ;
- enchaîne automatiquement extraction, initialisation, validations, promotions, applications, rendu et release jusqu’au prochain point éditorial ;
- produit des ZIP minimaux `wikidebia-chatgpt-review-package-1.0` avec séparation `editable/` / `context/` ;
- vérifie provenance locale, manifeste, contexte, baseline locale, structure ZIP et absence de fichiers supplémentaires ;
- restaure transactionnellement le répertoire de contrôle si la finalisation d’un retour échoue ;
- orchestre graphe, métadonnées françaises, contenu/documentation française, traduction/documentation anglaise et convergence sémantique ;
- rouvre la traduction et recommence les deux passes sémantiques lorsqu’une erreur certaine est trouvée ;
- ajoute `outgoing/` aux zones privées exclues de Git ;
- conserve toutes les primitives détaillées et tous les garde-fous de publication existants.

## 2.16.1 — 11 août 2026 — reprise ergonomique après validation initiale

- n’interrompt plus l’orchestration avant la revue des métadonnées pour les seuls défauts de forme/autonomie de titres importés que cette revue peut corriger ;
- conserve le blocage immédiat des incohérences réellement structurelles du graphe ;
- remplace le message opaque de validation initiale par un état `blocked_technical` avec codes/messages concrets ;
- produit automatiquement `outgoing/<debate_id>_initial_validation_diagnostic.zip`, limité aux rapports, graphe, registre, imports et contexte nécessaires, sans secret ;
- une simple relance de `workflow` réessaie la validation bloquée après mise à jour/correction et poursuit ensuite normalement ;
- ajoute des tests d’intégration sur le paquet de diagnostic et la reprise.

