# Migration 2.15.44

La norme 1.2.59 précise la création des futures traductions anglaises FR→EN. Une nouvelle page `Argument` anglaise ne publie jamais `|initialization=` : l’identifiant d’initialisation de la page française appartient au wiki source et ne peut pas être transféré au wiki anglais.

Pour toute nouvelle page anglaise traduite (Debate ou Argument), `|creation-date=` est une métadonnée de publication. Le corpus local peut porter une date provisoire de rendu, mais le plan de publication signé remplace cette valeur par la date civile du jour dans le fuseau de publication (Europe/Paris par défaut) au moment de la création distante. Si le jour change entre le plan et l’écriture, le plan est invalidé et doit être régénéré.

Une reprise après publication partielle conserve la `creation-date` déjà publiée uniquement si la révision distante courante est prouvée comme la révision de création de traduction (résumé individualisé et balises attendues). Aucun autre contenu de la page n’est modifié par cette normalisation.
