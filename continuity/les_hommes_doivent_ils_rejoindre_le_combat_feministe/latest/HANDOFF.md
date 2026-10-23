# Handoff — Les hommes doivent-ils rejoindre le combat féministe ?

- Branche : `codex/traduction-combat-feministe`
- Correctifs GitHub synchronisés jusqu’à : `36be15c`
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

## Correction des paramètres de relations vides

Le premier checkpoint ajoutait à tort `justifications` et `objections` avec une
valeur vide sur les pages sans relation correspondante. Le correctif générique
`74b1d26` impose désormais l’omission canonique de ces paramètres dans le
checkpoint de graphe.

Le plan correctif signé
`runtime/fr-publication/graph/empty-relation-parameter-restoration-plan.json`
porte l’empreinte
`0b67e8983509c9d97682585fa8fcb1abb8d43a9a23acae3abdf6836945fbc5a4`.
Il a retiré 90 paramètres `justifications` vides et 75 paramètres `objections`
vides sur 93 pages. Les 93 révisions ont été contrôlées sous l’identité
`ChatGPT`, avec la balise `chatgpt`.

Le reçu porte l’empreinte
`31ad1aae68486cf1ef8a40a52260d59f085aa278fd8a0a103449968212fc52c6`.
Une relecture distante indépendante des 100 arguments n’a trouvé aucun
paramètre vide restant ni aucune divergence avec le reçu ; elle est consignée
dans
`runtime/fr-publication/graph/empty-relation-parameter-restoration-verification.json`.

## Prochaine étape

La revue du contenu français est terminée pour 100 arguments et son ZIP complété
porte l’empreinte
`26d3c3de52b9d90a837d58bb73bef66bba7ccaa746b7564bdb1029823fe7cb07` :

```text
reviews/les_hommes_doivent_ils_rejoindre_le_combat_feministe_fr_content_review.zip
```

Le ZIP doit être placé dans `incoming/`, puis importé avec :

```bash
./wikidebia review-import les_hommes_doivent_ils_rejoindre_le_combat_feministe
```

Cette commande finalisera la revue française de contenu et déclenchera le second
checkpoint français. La traduction anglaise ne doit commencer qu’après ce second
checkpoint.

La revue conserve exactement les 22 résumés historiques et les 78 absences de
résumé, ainsi que les sept citations. Elle normalise de façon traçable les
capitales de noms communs, l’orthographe d’« émotions » et les variantes
singulier/pluriel, puis ajoute un concept distinctif aux pages auparavant
classées par le seul terme « féminisme ». Les deux références web historiques
(Slate pour A0012 et France Inter pour A0041) sont conservées dans le registre
contrôlé ; aucun texte historique n’est réécrit.

## Accès distant

L’accès API français et l’identité `ChatGPT@Codex-FR` ont été vérifiés. Aucun
secret ni fichier privé n’est présent dans cette sauvegarde. Le secret anglais
est injecté dans l’environnement, mais l’identité essayée `ChatGPT@Codex-EN` a
été refusée par le wiki anglais et ne doit pas être considérée comme prête.

Le mot de passe anglais a été renouvelé dans l’environnement le 23 octobre ;
l’identité devra être retestée sans journaliser ni versionner le secret avant la
première publication anglaise.

## Portabilité des reprises

La reprise a révélé que
`reports/initial_validation_execution.json` : les anciennes versions y
enregistraient deux chemins absolus et incluaient pourtant ce fichier dans
l’empreinte du build. Son assainissement légitime rendait alors la revue
inutilisable sur une autre machine. La trace non normative est maintenant hors
de l’empreinte portable, avec une compatibilité ancienne limitée aux deux
champs concernés et vérifiée par le SHA-256 historique.

## Vérification

Vérifier `SHA256SUMS` avant restauration. Le commit Git contenant ce fichier est
le commit de référence du snapshot ; les états antérieurs restent dans
l’historique de la branche.
