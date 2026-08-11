# Audit de régression kit 2.16.6

Base vérifiée : commit GitHub `5eca765`, versions 1.2.77 / 0.4.80 / 2.16.5.

Le correctif est limité à la cohérence des snapshots importés et de leur provenance après les actions structurelles de graphe. Les protections de 2.16.5 (préflight global, garde de révision, identité, droits, balise `chatgpt`, relecture bornée, reprise idempotente, validation prospective et ordre des mutations) sont conservées.

Régressions ajoutées :
- `apply_local_result` actualise l’empreinte brute et la taille de chaque fichier `update`/`redirect` ;
- un état reproduisant exactement le défaut 2.16.5 est réparé avant le workspace ;
- une dérive locale sur une page non attestée par les actions reste refusée par `read_import_metadata`.
