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

## 2.16.2 — 11 août 2026 — short_code ASCII et reprise sans reset

- dérive le `short_code` automatique depuis le `debate_id` canonique ASCII plutôt que depuis les initiales Unicode du titre ;
- `revenu_de_base` produit déterministement `RDB` ;
- répare automatiquement un workflow existant dont `short_code` est absent ou invalide avant l’initialisation du corpus ;
- accepte `--short-code` lors de cette reprise sans exiger la suppression de `.state/workflows/...` ;
- conserve et protège un code déjà valide en refusant une valeur explicite contradictoire ;
- ajoute des régressions sur le titre « Un revenu de base doit-il être instauré ? », le corpus-init direct et la reprise du workflow.
## 2.16.3 — 11 août 2026 — correction de la boucle de rejet du graphe

- corrige `review-import`, qui ne passe plus inconditionnellement à `promote_and_workspace` après `finalize_graph_review` ;
- un résultat `rejected` ouvre désormais `graph_correction` et produit automatiquement un paquet ChatGPT ;
- ajoute le contrat `wikidebia-graph-correction-1.0` et un moteur déterministe de reconstruction des placements, relations, profondeurs, branches, rôles et compteurs ;
- valide la correction avant reprise et restaure transactionnellement le build en cas d’échec ;
- prépare obligatoirement une nouvelle revue complète du graphe après correction, sans promotion implicite ;
- ajoute des tests de rejet, correction valide, correction invalide/rollback et absence de promotion.
## 2.16.4 — 11 août 2026 — exécution des décisions structurelles de revue

- ajoute `--execute-graph-actions` à `review-import` pour appliquer en une commande les décisions explicites `remove`, `merge_redirect`, `move` et `relation_change` ;
- retire les modèles de relation des pages mères et transforme les doublons en `#REDIRECTION [[page conservée]]` ;
- produit un résumé MediaWiki individualisé par page, avec `[[destination]]` obligatoire dans le résumé de retrait d’un doublon ;
- valide la projection locale complète avant la première écriture distante, puis préflight toutes les pages et revérifie chaque révision avant mutation ;
- relit contenu, résumé et balise `chatgpt` après chaque édition ;
- accepte de façon étroite les décisions propriétaires déjà inscrites dans certains ZIP 2.16.2/2.16.3 ;
- reconstruit le graphe et prépare une nouvelle revue complète sans promotion implicite.
## 2.16.5 — 11 août 2026 — relecture post-écriture bornée et reprise idempotente

- applique aux actions structurelles la même politique de relecture bornée déjà utilisée par la publication et les mises à jour ordinaires ;
- tolère le retard temporaire de visibilité d’une nouvelle révision et de la balise `chatgpt` après `action=edit` ;
- distingue les échecs de contenu, résumé, identifiant et balise au lieu d’un diagnostic générique ;
- lors d’une relance après exécution partielle, accepte un état final déjà présent uniquement si la révision courante porte exactement le contenu, le résumé et la balise attendus ;
- ajoute des tests de retard de réplica/balise et de reprise sans réécriture d’une page déjà correctement modifiée.

## 2.16.6 — 11 août 2026 — cohérence de la provenance après actions structurelles

- met à jour `sha256` et `size_bytes` de `data/import_provenance.json` après toute action de graphe qui réécrit un snapshot local (`update` ou `redirect`) ;
- répare automatiquement les états 2.16.4/2.16.5 déjà exécutés uniquement lorsque `graph_action_decisions.json` atteste le chemin, l’empreinte post-action exacte et une révision distante avancée ;
- laisse toute autre divergence de provenance bloquante, sans normalisation ni adoption silencieuse ;
- exécute cette réparation étroite avant la création/reprise du workspace éditorial afin d’éviter le blocage `Empreinte de provenance divergente` sur une modification effectuée par le kit lui-même ;
- ajoute des régressions couvrant la mise à jour immédiate de provenance, la reprise du défaut 2.16.5 et le maintien du blocage d’une dérive non attestée.


## 2.16.7 — 11 août 2026 — reprise de provenance après plusieurs vagues de corrections du graphe

- corrige la reprise 2.16.6 lorsque plusieurs séries d’actions structurelles ont été exécutées : `reviews/graph_action_decisions.json` ne conserve que la dernière série, tandis que les séries antérieures restent attestées dans `.state/graph-actions/<débat>/` ;
- agrège, pour la réparation de compatibilité uniquement, les plans et reçus historiques dont les schémas, identifiants de débat et empreintes internes sont valides ;
- exige que le contenu local corresponde exactement à `desired_sha256` et que la révision de provenance corresponde à la révision réellement écrite par le reçu avant de rafraîchir `sha256` et `size_bytes` ;
- ne réexécute aucune écriture distante et laisse toute dérive non attestée bloquante ;
- ajoute une régression reproduisant deux vagues de corrections où l’audit courant a écrasé l’attestation de la première vague.
## 2.16.8 — 11 août 2026 — import de revue transactionnel et cohérence de release

- `review-import` conserve désormais une sauvegarde transactionnelle jusqu’à la réussite de l’avancement mécanique suivant.
- En cas d’échec local après acceptation d’une revue, la base, le workflow et les artefacts mécaniques nouvellement créés sont restaurés ; le même paquet de revue reste réimportable.
- Les actions de graphe déjà écrites à distance sont traitées comme une frontière irréversible explicite et restent enregistrées pour reprise, sans faux rollback local.
- La réparation de provenance est documentée et testée comme mécanisme fondé sur preuves/schémas plutôt que sur le numéro du kit producteur.
- Pour les versions installées à partir de 2.16.8, `upgrade` ne requiert plus l’égalité du triplet répété dans les trois composants : chaque composant fait autorité pour sa propre version, les versions étrangères restant de la provenance.
- La fabrication de release est assortie d’un contrôle explicite garantissant que les trois `VERSIONS.json` embarqués sont identiques.

## 2.16.9 — 12 août 2026 — revue différentielle des métadonnées préexistantes

- propage `page_origin=preexisting` dans les paquets de revue issus d’un corpus extrait du wiki ;
- ne requiert plus `displayed_title_complete_proposition=true` pour un `titre-affiché` historique préexistant et ne le réécrit pas pour la seule raison qu’il est nominal ;
- conserve les exigences complètes de création pour les pages/titres nouveaux ;
- ne bloque plus une page préexistante parce qu’elle dépasse la cible de mots-clés de création ;
- vérifie qu’aucun mot-clé historique n’a été retiré, sauf correction explicitement décrite ou suppression `clearly_irrelevant` accompagnée d’une justification ;
- autorise corrections de casse/graphie, réordonnancement et ajouts de mots-clés ;
- ajoute les consignes correspondantes directement dans les ZIP `fr_metadata_review` et des tests de non-régression.

## 2.16.10 — 12 août 2026 — faux positif « Il ne faut »

- corrige `WDV-EDT-016` via le validateur aligné : `Il ne faut…` est reconnu comme tournure impersonnelle, au même titre que `Il faut…` ;
- maintient le blocage des pronoms réellement anaphoriques comme `Il réduit…` lorsque leur référent est extérieur au titre ;
- ajoute une régression explicite sur le titre réel `Il ne faut pas instaurer plus de temps libre` ;
- aucune règle éditoriale n’est assouplie et la norme reste 1.2.78.

## 2.16.11 — 12 août 2026 — provenance retirée et revue de contenu

- conserve dans `import_provenance.json` les pages retirées du graphe afin de préserver leur traçabilité ;
- exclut de la couverture active de la revue de contenu uniquement les lignes explicitement marquées `retired_redirect` ou `retired_deleted` ;
- continue de bloquer toute ligne de provenance supplémentaire non explicitement retirée et toute absence de provenance pour un nœud actif ;
- ajoute des tests positif et négatif de non-régression.

## 2.16.12 — 12 août 2026 — résumés individualisés des reprises de corpus

- chaque nouveau plan `update --archive` déclare `edit_summary_contract=page_specific_v1` ;
- les opérations `create`, `update`, `move`, `redirect` et `delete` portent toutes une politique et un résumé MediaWiki propres ;
- une mise à jour ordinaire calcule son résumé à partir des paramètres réellement modifiés (`résumé`, références, rubriques, mots-clés, introduction, plan argumentatif, etc.) ;
- l’ajout interlangue français conserve son résumé spécialisé avec wikilien anglais ;
- les renommages, redirections et suppressions reçoivent des résumés spécifiques à leur opération ;
- l’exécuteur recalcule le résumé attendu avant chaque écriture, refuse une divergence ou `Corrections`, puis vérifie le résumé dans la révision relue ;
- les plans historiques sans contrat individualisé conservent leur voie de compatibilité ;
- les tests couvrent les cinq familles de mutations et le refus du résumé générique.

## 2.16.13 — 12 août 2026 — publication française automatique avant traduction

- fait de la réussite de `fr_content_review` une frontière distante : rendu FR sans interlangue, plan signé, publication/attestation, puis seulement préparation anglaise ;
- réutilise le moteur de reprise 2.16.12 et ses résumés MediaWiki individualisés, gardes de révision et vérifications post-écriture ;
- conserve le plan/reçu et reprend idempotemment après interruption, y compris si la publication a réussi mais que la préparation anglaise échoue ensuite ;
- répare les workflows déjà arrêtés sur un paquet anglais produit avant cette règle en publiant d’abord le checkpoint français manquant ;
- déplace l’UX de retour vers `incoming/` : `./wikidebia review-import` pour un seul paquet, `./wikidebia review-import <debate_id>` en cas de pluralité ;
- sélectionne par `REVIEW_PACKAGE.json.debate_id`, archive le ZIP après succès et le conserve dans `incoming/` après échec ;
- valide `document_kind` directement dans `sources_working.json` avant la projection finale.
