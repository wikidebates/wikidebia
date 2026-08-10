# Wikidéb’IA — Kit 2.15.38

## Nouveautés 2.15.38

Le workflow de traduction consigne désormais formellement la provenance réelle des recherches de `name=` dans le format de revue 1.1. Chaque `Quote` reçoit une attestation de complétude ; un ratio lexical FR→EN inférieur à 0,60 impose une seconde revue explicite, sans devenir une règle de réécriture.

Le scellement de release génère `release/content_inventory.json`, lie son SHA-256 et ses compteurs au reçu externe, puis recalcule l’inventaire après extraction fraîche du ZIP exact.

Le kit reste aligné sur la norme 1.2.61 et le validateur 0.4.64.

## Revue adaptative 2.15.38
Le kit calcule un profil de densité à partir de la source française, propose des unités 10/8/6/5, exige leur clôture indépendante, applique le format `name=` 1.2 et propage les attestations structurées sujet/prédicat/portée/modalité.
