# Migration vers le kit 2.2.12

Le kit 2.2.12 utilise le validateur 0.4.27 et la norme 1.2.25.

La reprise distante est durcie :

- toute opération `manual_review` bloque l’exécution avant la première écriture ;
- un plan sans opération exécutable renvoie `no_changes` sans produire de faux reçu de succès ;
- `./wikidebia update IDENTIFIANT` privilégie le corpus installé ;
- une archive se sélectionne explicitement avec `--archive SÉLECTEUR` ;
- les archives de reprise sont extraites dans une zone de staging avant toute adoption ;
- `--dry-run` ne modifie jamais le corpus actif.

Le kit 2.2.13 complétera ensuite ce protocole avec l’attestation distante des plans entièrement `skip`, `no_changes_in_scope`, le nettoyage systématique du staging et la conservation signée des suppressions différées.
