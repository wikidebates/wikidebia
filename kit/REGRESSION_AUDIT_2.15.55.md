# Audit de régression kit 2.15.55

- 372 tests réussis ;
- anciens rapports de validateur pré-schémas normalisés à l’entrée ;
- labels historiques `wikidebia-publication-plan-X.Y.Z` normalisés vers `wikidebia-publication-plan-1.0` ;
- aucun workflow opérationnel hors gestionnaire d’installation ne compare la release du producteur à la release courante ;
- les contrôles d’intégrité restent liés aux schémas, SHA-256, révisions distantes et preuves signées ;
- `./wikidebia upgrade` conserve l’égalité exacte du triplet de composants et l’anti-downgrade, car ces contrôles portent sur l’installation d’une release cohérente, non sur la lecture d’un artefact.
