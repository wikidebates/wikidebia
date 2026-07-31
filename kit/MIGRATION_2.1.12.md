# Migration vers le kit 2.1.12

1. Installer le lanceur racine `wikidebia` et le modèle `.gitignore` fournis dans `root_template/`.
2. Déplacer `user-config.py` et `user-password.cfg` vers `private/pywikibot/`.
3. Déposer les débats dans `incoming/debates/` et les mises à jour dans `updates/`.
4. Utiliser `./wikidebia publish --scope …` pour publier ; la page Débat/Debate est traitée avant les arguments dans chaque langue.
5. Utiliser `./wikidebia update` pour installer les composants, archiver les versions précédentes, vider `updates/` et synchroniser Git.
6. Initialiser une fois le dépôt distant avec `./wikidebia github-init URL_DU_DEPOT`.

Les chemins absolus ne doivent figurer dans aucun fichier suivi ou rapport persistant.
