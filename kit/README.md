# Wikidéb’IA — Kit 2.15.49

Version de réconciliation entre la lignée traduction/validation 2.15.38 et la lignée de publication GitHub 2.15.45 (commit `8b46816`), issues du kit 2.15.32 commun.

Le kit conserve les renforcements de traduction : validation différentielle FR→EN, revue sémantique structurée, portée des appellations consacrées, registre documentaire global, complétude des `Quote`, score de risque des unités de revue, inventaire transactionnel de release et validation de l’archive exacte après extraction fraîche.

Il intègre également les mécanismes de publication déjà utilisés sur les wikis : résumés MediaWiki individualisés, balises `chatgpt` + `translated-fr`, rattrapage audité de `translated-fr`, reprise `--interlanguage-only`, relecture bornée des balises, résolution sûre de la révision de création, `nom-consacré` / `established-name`, absence d’`initialization` sur une nouvelle traduction anglaise et `creation-date` fixée au jour réel de publication.

Les numéros 2.15.33 à 2.15.38 ont été réutilisés différemment dans les deux branches parallèles. Leur historique exact est conservé sous `branch_history/`; la version 2.15.46 est le premier point de réconciliation.

La version 2.15.48 corrige la dépendance à l’ordre de collecte de deux modules de tests et aligne le kit sur le validateur 0.4.67 ; le premier point de réconciliation historique reste 2.15.46.

La version 2.15.49 ajoute un garde-fou croisé empêchant le retour de formulations actives obsolètes dans le paquet Normes et s’aligne sur 1.2.65 / 0.4.68.
