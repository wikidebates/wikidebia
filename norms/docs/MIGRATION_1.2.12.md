# Migration vers la norme 1.2.12

1. Installer le validateur 0.4.12 et le kit 2.1.12.
2. Installer le lanceur racine et les dossiers `incoming/debates`, `updates` et `private/pywikibot`.
3. Déplacer les secrets Pywikibot historiques vers `private/pywikibot/`.
4. Initialiser le dépôt Git/GitHub et appliquer le `.gitignore` fourni.
5. Utiliser `./wikidebia publish --scope …` et `./wikidebia update`.
6. Vérifier qu’aucun fichier persistant ne contient le chemin absolu de l’installation.
