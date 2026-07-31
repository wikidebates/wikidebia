# Migration vers la norme 1.2.13

1. Installer le validateur 0.4.13 et le kit 2.1.13.
2. Déplacer les ZIP de débats directement dans `incoming/`; ne plus utiliser `incoming/debates/`.
3. Nommer chaque archive `<debate_id>.zip`; aucun suffixe `release_ready` n’est demandé.
4. Lancer `./wikidebia publish` lorsqu’un seul ZIP est présent, ou `./wikidebia publish IDENTIFIANT` lorsqu’il y en a plusieurs.
5. Vérifier que le nom du ZIP correspond exactement au `debate_id` du manifeste.

Les ZIP encore présents dans l’ancien dossier `incoming/debates/` sont migrés automatiquement vers `incoming/` pendant la mise à jour. Toute collision de noms avec un contenu différent bloque l’opération sans écrasement.
