# Migration vers la norme 1.2.15

1. Installer les composants 1.2.15 / 0.4.15 / 2.1.15.
2. Ne modifier aucun champ `normative_versions` des corpus historiques uniquement pour publier.
3. Lancer `./wikidebia publish`; le kit exécute le validateur 0.4.15 sur la norme déclarée par le corpus.
4. Corriger le corpus seulement si cette validation courante détecte une erreur réelle.
