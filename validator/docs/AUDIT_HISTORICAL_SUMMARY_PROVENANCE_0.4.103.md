# Audit — provenance historique des résumés 0.4.103

Statut : PASSED

Le diagnostic réel du vote électronique a montré que `wikicode.py` et `editorial.py`
partageaient accidentellement le même cache tout en calculant des ensembles différents.
La portée `wikicode`, exécutée la première, ne reconnaissait pas
`historical_authorized_change` et empoisonnait le cache utilisé ensuite par la portée
éditoriale.

Le correctif centralise le calcul dans `historical_summary.py`. Une régression reproduit
l’ordre réel des portées et vérifie que les cinq statuts historiques supportés ne peuvent
plus diverger selon le contrôleur appelant.

Norme : 1.2.87
Kit : 2.16.37
