# Migration vers le kit 2.1.13

1. Remplacer le kit 2.1.12 par le kit 2.1.13.
2. Utiliser `incoming/` comme dossier unique des ZIP de débats ; le sous-dossier `incoming/debates/` n’est plus utilisé.
3. Renommer chaque archive en `<debate_id>.zip`. Aucun suffixe `release_ready` n’est demandé.
4. Lorsque `incoming/` contient un seul ZIP, lancer `./wikidebia publish`. Lorsqu’il en contient plusieurs, lancer `./wikidebia publish IDENTIFIANT`.
5. Ne pas inclure `.zip` dans l’identifiant. Le kit vérifie que le nom du fichier correspond exactement au `debate_id` interne.

Lors de `./wikidebia update`, les ZIP présents dans l’ancien dossier `incoming/debates/` sont déplacés automatiquement vers `incoming/`. Une collision de noms avec des contenus différents bloque la migration et conserve une copie dans l’archive de mise à jour.
