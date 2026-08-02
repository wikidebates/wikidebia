# Migration vers le kit 2.2.13

Le kit 2.2.13 remplace le comportement incomplet de 2.2.12.

- un plan entièrement `skip` est attesté à distance et renouvelle l’état publié signé sans écriture MediaWiki ;
- toute archive de reprise exige `--archive`, sans repli implicite ;
- les zones de staging sont supprimées à chaque sortie ;
- une portée sans opération sélectionnée renvoie `no_changes_in_scope` ;
- `--no-delete` conserve les pages différées avec le statut `pending_delete`, afin que `--only-delete` puisse les reprendre ;
- `manual_review` et `blocked` restent strictement bloquants.
