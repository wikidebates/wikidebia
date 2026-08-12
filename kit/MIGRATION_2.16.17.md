# Migration 2.16.17 — consentement explicite pour les textes historiques

Cette migration remplace l’immutabilité absolue de 2.16.16 par une protection par défaut avec consentement propriétaire scoped.

Les anciens paquets `fr_content_review` au schéma supporté sont normalisés d’après leur contenu, sans égalité de version producteur : un delta historique ancien dépourvu de demande structurée est conservé comme `suggested_change` puis remis à `keep`; les décisions de rubriques, mots-clés et documentation sont conservées. Un delta explicitement décrit par `historical_change_request` peut être autorisé sans refaire la revue.

Un ZIP ne peut pas fabriquer son propre consentement. Après approbation du propriétaire, `./wikidebia review-import --authorize-historical-changes` scelle localement l’archive retournée, son `package_id`, son manifeste, les champs et leurs SHA avant/après. Le checkpoint français n°2 publie ensuite les deltas autorisés ; aucune troisième publication n’est ajoutée.
