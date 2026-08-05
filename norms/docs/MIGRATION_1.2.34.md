# Migration vers la norme 1.2.34

## Publication française avant traduction

Ajouter au manifeste :

```json
"translation_status": {"en": "deferred"}
```

Laisser les titres anglais à `unassigned` ou absents, ne pas créer de pages anglaises et retirer tout lien interlangue fictif des nouvelles pages françaises. Lancer ensuite `./wikidebia update --archive <archive> --scope fr --dry-run`, puis la même commande sans `--dry-run`.

## Ajout ultérieur de l’anglais

Après traduction, passer le statut à `ready` ou `published`, verrouiller les titres anglais, ajouter les pages anglaises au manifeste, valider la portée anglaise, puis effectuer une reprise française pour ajouter les liens exacts.

## Non-régression

Ne pas appliquer `deferred` à un corpus déjà bilingue. Un lien valide existant n’est pas supprimé automatiquement. Un titre anglais `locked` vide, une cible vide ou divergente, une page anglaise sans titre valide et une portée anglaise différée restent bloquants.
