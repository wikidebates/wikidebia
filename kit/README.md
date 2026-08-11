# Wikidéb’IA Kit 2.16.9

Le kit 2.16.9 applique la politique différentielle de reprise des métadonnées : les pages déjà présentes sur le wiki conservent par défaut leurs `titre-affiché` et mots-clés historiques. La propositionnalité complète et les cibles quantitatives restent des règles de création pour les nouvelles pages/titres générés par IA. Les titres canoniques restent corrigibles ; les mots-clés historiques peuvent être corrigés et complétés, et ne sont retirés qu’en cas de non-pertinence réelle explicitement justifiée.

# Wikidéb’IA Kit 2.16.8
Le kit 2.16.8 rend `review-import` transactionnel pour toutes les transitions locales jusqu’au prochain arrêt éditorial : si l’avancement mécanique échoue, la revue reste réimportable et le workflow, la base et les artefacts créés pendant la tentative sont restaurés. Les écritures distantes de corrections du graphe restent une frontière irréversible explicite et sont conservées avec leurs plans/reçus pour une reprise déterministe. La réparation de provenance repose sur les preuves de contenu et les schémas/capacités, pas sur l’égalité du numéro de kit. `upgrade` donne aussi désormais le détail des jeux de versions divergents entre composants.

Le kit 2.16.7 part du commit GitHub `5eca765` (1.2.77 / 0.4.80 / 2.16.5) et corrige la provenance locale après exécution des décisions structurelles du graphe. Les fichiers `imports/fr/**/*.wiki` modifiés par une action `update` ou `redirect` mettent désormais immédiatement à jour leur `sha256` et leur taille dans `data/import_provenance.json`. Pour les états déjà produits par 2.16.4/2.16.5, la reprise répare automatiquement uniquement les fichiers attestés par `reviews/graph_action_decisions.json`, dont le contenu courant correspond exactement à l’empreinte post-action prévue et dont la révision distante a avancé. Toute dérive non attestée reste bloquante.

Historique 2.16.1 : une anomalie éditoriale de titre importé ne bloque plus avant la revue qui doit précisément la corriger. Les incohérences structurelles restent bloquantes ; lorsqu’elles surviennent, `workflow` affiche leurs codes/messages et produit automatiquement un ZIP de diagnostic minimal sous `outgoing/`. Après correction, relancer la même commande reprend la phase sans reset manuel. Le mécanisme général de paquets de revue introduit en 2.16.0 reste inchangé.

Les paquets de revue utilisent le schéma stable `wikidebia-chatgpt-review-package-1.0`, séparent `editable/` et `context/`, lient leur provenance à l’état local, refusent les fichiers supplémentaires et excluent les secrets. La convergence sémantique est elle aussi orchestrée : une erreur certaine rouvre la traduction, puis les deux passes indépendantes recommencent. Le workflow normal ne publie rien à distance. L’unique exception pré-W11 est l’option explicite `review-import ... --execute-graph-actions`, réservée aux décisions structurelles déjà inscrites dans une revue du graphe.

## Notes héritées du paquet parent 2.15.54

Version de réconciliation entre la lignée traduction/validation 2.15.38 et la lignée de publication GitHub 2.15.45 (commit `8b46816`), issues du kit 2.15.32 commun.

Le kit conserve les renforcements de traduction : validation différentielle FR→EN, revue sémantique structurée, portée des appellations consacrées, registre documentaire global, complétude des `Quote`, score de risque des unités de revue, inventaire transactionnel de release et validation de l’archive exacte après extraction fraîche.

Il intègre également les mécanismes de publication déjà utilisés sur les wikis : résumés MediaWiki individualisés, balises `chatgpt` + `translated-fr`, rattrapage audité de `translated-fr`, reprise `--interlanguage-only`, relecture bornée des balises, résolution sûre de la révision de création, `nom-consacré` / `established-name`, absence d’`initialization` sur une nouvelle traduction anglaise et `creation-date` fixée au jour réel de publication.

Les numéros 2.15.33 à 2.15.38 ont été réutilisés différemment dans les deux branches parallèles. Leur historique exact est conservé sous `branch_history/`; la version 2.15.46 est le premier point de réconciliation.

La version 2.15.48 corrige la dépendance à l’ordre de collecte de deux modules de tests et aligne le kit sur le validateur 0.4.67 ; le premier point de réconciliation historique reste 2.15.46.

La version 2.15.50 ajoute un garde-fou croisé empêchant le retour de formulations actives obsolètes dans le paquet Normes et s’aligne sur 1.2.66 / 0.4.69.

La version 2.15.51 étend la preuve propositionnelle : changement de forme idiomatique sous revue explicite, corpus versionné de régressions réelles, catalogue de marqueurs aligné avec le validateur et preuves sémantiques de champ pour Debate/Argument. Elle s’aligne sur 1.2.67 / 0.4.70.

La version 2.15.52 durcit la preuve d’indépendance des passes et les régressions keyword/parsing, sans changer les règles éditoriales.

La version 2.15.53 émet les paramètres MediaWiki `sujet-développé` / `expanded-topic` et `débat-dédié` / `dedicated-debate`, tout en lisant les anciens noms dans les corpus historiques.

La version 2.15.54 corrige l’alignement du validateur sur les métadonnées de première publication anglaise : aucune projection cross-wiki d’`initialization`, et aucune égalité imposée entre `creation-date` anglaise et `date-création` française.

## Architecture de compatibilité 2026-08-10

Les numéros de release sont une provenance. La compatibilité opérationnelle est pilotée par `CAPABILITIES.json` et les identifiants/version de schéma ; les égalités exactes sont réservées à l’installation, l’anti-downgrade, la reproductibilité et l’audit.
