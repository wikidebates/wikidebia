# Architecture du validateur 0.4.38

Le validateur sépare schémas, cohérence, graphe, lots, sources, fichiers, wikicode, bilinguisme, éditorial, workflow et plans distants. Sous la norme 1.2.32, il conserve le contrôle du rendu déterministe des liens interlangues et des citations, et son auto-audit vérifie aussi la cohérence des documents normatifs actifs. Il reste strictement local et en lecture seule.

## Traduction différée rétrocompatible 1.2.35

Le module `translation.py` centralise la lecture du statut anglais. Les portées `workflow`, `bilingual`, `editorial`, `wikicode`, `coherence` et `batches` appliquent la dérogation à toute norme historique 1.2.x prise en charge, uniquement lorsque le manifeste déclare explicitement `translation_status.en=deferred`.
