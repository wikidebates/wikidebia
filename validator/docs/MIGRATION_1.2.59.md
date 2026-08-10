# Migration 1.2.59 / validateur 0.4.62 / kit 2.15.36

La révision 1.2.59 ferme trois écarts de traçabilité observés pendant la vérification du corpus traduit :

1. le registre de recherche des appellations passe au format `wikidebia-argument-name-discovery-review-1.1` et distingue `actual_log`, `fresh_recheck` et `historical_reconstruction` ;
2. toute nouvelle `Quote` porte une attestation explicite de complétude ; un ratio lexical inférieur à 0,60 déclenche une seconde revue humaine documentée sans devenir une preuve automatique d'erreur ;
3. chaque release contient `release/content_inventory.json`, dont les compteurs et empreintes sont recalculés après extraction fraîche et liés au reçu externe.

Le format de revue des noms 1.0 reste lisible. Les champs historiques manquants ne sont jamais fabriqués rétroactivement.
