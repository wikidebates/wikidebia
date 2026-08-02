# Migration vers la norme 1.2.26

Cette migration ne change aucun contenu de débat. Elle corrige le protocole de reprise 1.2.25. Les installations doivent adopter le kit 2.2.13 et le validateur 0.4.28.

Les intégrations doivent employer `--archive` pour toute archive de reprise. Un résultat entièrement `skip` produit désormais une attestation signée `no_changes` et actualise l’état publié après relecture distante, sans édition MediaWiki. Les reprises en `--no-delete` conservent les pages différées avec le statut `pending_delete` jusqu’à leur traitement par `--only-delete`.
