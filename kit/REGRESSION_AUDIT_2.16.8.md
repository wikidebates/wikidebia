# Audit de régression kit 2.16.8

Contrôles ajoutés :

- échec après consommation provisoire d’une revue : restauration de `pending_review`, de la phase, du `work_id` et de la base ;
- échec après simulation de promotion et création partielle du workspace : suppression des artefacts créés pendant la transaction et restauration du build ;
- conservation du comportement de reprise pour les actions de graphe déjà écrites à distance ;
- réparation multi-vagues de provenance à partir des plans/reçus historiques ;
- diagnostic détaillé des divergences de `VERSIONS.json` entre composants ;
- contrôle de cohérence du paquet complet avant livraison.
