# Handoff — Les hommes doivent-ils rejoindre le combat féministe ?

- Branche : `codex/traduction-combat-feministe`
- Correctifs GitHub synchronisés jusqu’à : `317dbbe`
- Commit de référence du snapshot : commit contenant ce fichier
- Date du snapshot : 23 octobre 2026
- Phase : `fr_content_review`
- Statut : `awaiting_review`
- Work actif : `EDIT-20261023-001`
- Work remplacé : `EDIT-20261022-001`

## Correction des titres affichés

Le Work initial modifiait les titres affichés de pages françaises sources. Son
exécution a été interrompue après dix-neuf mises à jour et avant tout renommage.
Six lignes `titre-affiché` effectivement modifiées ont été restaurées sur le wiki
français, avec contrôle de révision, identité `ChatGPT`, balise `chatgpt` et
relecture après écriture.

Le correctif générique `317dbbe` interdit désormais toute modification du titre
affiché d’une page source préexistante. Un nouveau Work a été construit depuis le
corpus promu. Sa revue conserve les 100 titres affichés historiques et garde les
dix corrections de titres canoniques : A0024, A0043, A0059, A0074, A0075,
A0077, A0084, A0085, A0096 et A0099. Le validateur a accepté le Work corrigé.

## Checkpoint français graphe et titres

Les sept révisions que le nouveau préflight ne pouvait plus rattacher au snapshot
initial ont été réconciliées uniquement après vérification de leur chaîne : toutes
étaient signées par `ChatGPT`, portaient la balise `chatgpt`, utilisaient un résumé
attendu et remontaient directement à la révision source.

Le plan final signé
`runtime/fr-publication/graph/update-plan.json` porte l’empreinte
`2e934627a817399ad9ab8887c99df8b915d027e7e130385cc0352c2c2c3d3d67` :
77 mises à jour, dix renommages, quatorze pages déjà conformes, aucune revue
manuelle et aucun blocage. Son exécution et sa vérification ont réussi. Le reçu
de checkpoint `runtime/fr-publication/graph/publication-receipt.json` porte
l’empreinte
`69af472f704df97375b319f1b33e9bbde45598d5d884b27ef852882da9cf9767`.

La restauration ciblée et la réconciliation de l’exécution interrompue restent
attestées dans :

- `runtime/fr-publication/graph/displayed-title-restoration-plan.json` ;
- `runtime/fr-publication/graph/displayed-title-restoration-receipt.json` ;
- `runtime/fr-publication/graph/interrupted-checkpoint-reconciliation.json`.

## Prochaine étape

La revue du contenu français est préparée pour 100 arguments :

```text
reviews/les_hommes_doivent_ils_rejoindre_le_combat_feministe_fr_content_review.zip
```

Après revue éditoriale, placer le ZIP corrigé dans `incoming/`, puis lancer :

```bash
./wikidebia review-import les_hommes_doivent_ils_rejoindre_le_combat_feministe
```

Cette commande finalisera la revue française de contenu et déclenchera le second
checkpoint français. La traduction anglaise ne doit commencer qu’après ce second
checkpoint.

## Accès distant

L’accès API français et l’identité `ChatGPT@Codex-FR` ont été vérifiés. Aucun
secret ni fichier privé n’est présent dans cette sauvegarde. Le secret anglais
est injecté dans l’environnement, mais l’identité essayée `ChatGPT@Codex-EN` a
été refusée par le wiki anglais et ne doit pas être considérée comme prête.
