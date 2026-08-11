# Audit de non-régression — kit 2.16.11

- provenance d’un nœud actif absente : blocage maintenu ;
- provenance supplémentaire `active_import` : blocage maintenu ;
- provenance supplémentaire explicitement `retired_redirect` / `retired_deleted` : conservée pour l’audit et ignorée par la couverture active ;
- la revue de contenu ne contient que les nœuds `status=active` du registre ;
- aucune règle éditoriale, aucun schéma et aucun comportement distant n’est modifié.
