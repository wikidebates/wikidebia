# Migration 2.15.23

Cette maintenance corrige la rationalisation des sources produites par `./wikidebia upgrade`.

Après mise à niveau, la racine conserve uniquement `WIKIDEBIA_SOURCE_ACTIVE.md` et `WIKIDEBIA_SOURCE_PACKAGE_RECEIPT.json` pour la documentation active. Les anciens fichiers `WIKIDEBIA_NORMES_ACTIVES.md`, `WIKIDEBIA_VALIDATEUR_ACTIF.md` et `WIKIDEBIA_RECUS_ARCHIVES.json` sont déplacés dans l’archive de sauvegarde de la mise à niveau, puis ne sont plus régénérés.
