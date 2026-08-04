# Migration vers le kit 2.4.0

Le kit 2.4.0 ajoute `./wikidebia corpus-init-from-snapshot`.

Cette commande transforme une extraction auditée en corpus local `graph_draft`. Elle conserve les pages distantes sous `imports/fr/`, génère le registre maître, la projection du graphe, les identifiants déterministes, les fichiers de provenance et les registres de revue provisoires.

La commande ne publie rien, ne modifie aucun corpus actif et ne promeut pas le build vers `corpus/`. Les commandes `publish`, `update`, `upgrade` et `graph-extract` conservent leurs protections antérieures.

Le manifeste SHA-256 complet du paquet d’extraction est vérifié avant conversion. Le constructeur refuse les graphes ou snapshots altérés, les liens symboliques ZIP, les collisions de titres après normalisation et tout dossier de sortie situé hors de `.state/corpus-builds/`.

