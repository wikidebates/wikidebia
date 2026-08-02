# Migration vers le kit 2.2.13

Le kit 2.2.13 utilise le validateur 0.4.28 et la norme 1.2.26.

La reprise distante est durcie :

- toute opération `manual_review` bloque l’exécution avant la première écriture ;
- un plan sans opération exécutable renvoie `no_changes` et ne réécrit pas l’état publié ;
- `./wikidebia update IDENTIFIANT` privilégie toujours le corpus installé ;
- une archive doit être demandée explicitement avec `--archive SÉLECTEUR` lorsqu’un corpus homonyme existe ;
- les archives de reprise sont extraites dans une zone de staging et ne remplacent `corpus/` qu’après une exécution réussie, ou après une exécution réelle sans changement ;
- `--dry-run` ne modifie jamais le corpus actif.
