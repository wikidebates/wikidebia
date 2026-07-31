# Migration vers la norme 1.2.15

1. Déclarer `consolidated_norm=1.2.15`, le validateur 0.4.15 et le kit 2.1.15.
2. Conserver les ZIP directement dans `incoming/`.
3. Ne pas renommer une ancienne archive uniquement pour faire correspondre son nom au `debate_id`.
4. Avec un ZIP unique, lancer `./wikidebia publish`; avec plusieurs ZIP, fournir exactement le nom du fichier sans `.zip`.
5. Laisser le kit lire `manifest.debate_id`, qui détermine le dossier du corpus et la publication.
