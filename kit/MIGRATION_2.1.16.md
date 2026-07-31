# Migration vers le kit 2.1.17

1. Remplacer le kit 2.1.15 par le kit 2.1.17 avec `./wikidebia update`.
2. Le lanceur crée automatiquement `.venv/` lorsqu’il est absent ou inutilisable.
3. Il installe automatiquement les dépendances déclarées dans `requirements-runtime.txt`, notamment Pywikibot.
4. L’empreinte des exigences installées est conservée uniquement dans `.state/`, dossier exclu de Git.
5. `./wikidebia doctor` contrôle désormais l’interpréteur virtuel et les modules nécessaires.
6. Aucun environnement virtuel, cache, mot de passe ou cookie n’est ajouté au dépôt Git.
