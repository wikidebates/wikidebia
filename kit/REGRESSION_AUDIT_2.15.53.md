# Audit de régression — Kit 2.15.53

Le kit 2.15.53 conserve toutes les capacités de 2.15.52 et implémente la migration de paramètres MediaWiki 1.2.69.

- 361 tests pytest collectés et réussis en suite complète ;
- 361/361 également réussis avec ordre de fichiers inversé ;
- rendu courant exclusif : `sujet-développé` / `expanded-topic` et `débat-dédié` / `dedicated-debate` ;
- lecture des anciens noms à l'import/reprise puis normalisation vers les nouveaux noms sans altération de valeur ;
- l'ancien argument CLI `--follow-local-relations-at-detailed-debate` reste un alias de compatibilité du nouveau `--follow-local-relations-at-dedicated-debate` ;
- nouvelles capacités déclaratives : contrat de renommage, migration sûre des alias historiques et gates de non-régression dédiés ;
- aucune capacité déclarative du parent ou des trois lignées historiques n'a disparu.
