# Migration 2.15.37

Cette maintenance ajoute un mode de reprise française strictement limité aux liens interlangues :

```bash
./wikidebia update --scope fr --interlanguage-only --dry-run
./wikidebia update --scope fr --interlanguage-only
```

Le mode prend le wikicode distant courant comme base, conserve toutes ses autres valeurs et ajoute uniquement le lien vers le titre anglais correspondant au même `page_id`. Une redirection distante reste une redirection et reçoit un lien `[[en:Titre anglais]]`. Toute cible déjà liée vers un autre titre, toute page absente ou tout format distant non reconnu reste bloquant.
