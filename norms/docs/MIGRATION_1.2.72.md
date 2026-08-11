# Migration 1.2.72

Maintenance sans changement éditorial. Le correctif porte sur le kit `graph-extract` : l’option canonique `--follow-local-relations-at-dedicated-debate` et son alias historique convergent désormais vers le même attribut `argparse`, utilisé par le gestionnaire et l’extracteur. Les clés techniques internes de schéma `complete_topic` et `detailed_debate` restent inchangées, conformément à la migration 1.2.69.
