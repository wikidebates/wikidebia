# Migration 1.2.59 — création des traductions anglaises

La révision 1.2.59 ne migre aucune page déjà publiée. Elle précise uniquement le contrat des futures créations FR→EN.

## `initialization`

Une nouvelle page `Argument` anglaise issue d’une traduction ne transporte jamais `|initialisation=` ni sa forme anglaise `|initialization=` depuis le wiki français. Cet identifiant appartient à la relation de parenté sur le wiki source et n’est pas portable entre wikis. Une page anglaise préexistante conserve toutefois ses paramètres historiques selon la politique de préservation non destructive.

## `creation-date`

Pour une nouvelle page anglaise traduite, la valeur distante de `|creation-date=` est une métadonnée de publication. Elle vaut le jour civil où cette page est effectivement créée sur le wiki anglais, et non la valeur française de `|date-création=` ni une date de traduction/rendu local.

Le plan de publication signe la date prévue et le fuseau de publication (`Europe/Paris` par défaut). Juste avant chaque création anglaise, le kit revérifie le jour courant. Si le jour a changé, la création suivante est bloquée et un nouveau plan doit être généré. Les pages déjà créées conservent leur date historique ; les pages restantes reçoivent la date du nouveau jour lors de la reprise.

Une valeur locale de `creation-date` présente dans l’artefact traduit avant publication est donc provisoire pour une page nouvelle : elle est remplacée au moment de la création distante. Elle ne doit jamais être interprétée comme une traduction de `date-création`.
