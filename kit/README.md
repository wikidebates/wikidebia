# Wikidéb’IA — Kit 2.15.17

Kit de publication et de reprise aligné sur la norme 1.2.41 et le validateur 0.4.44.

Pour mettre à jour un débat, déposez son ZIP dans `incoming/` puis lancez `./wikidebia update`. Si ce ZIP est unique, il est sélectionné automatiquement et la portée `all` est utilisée. En présence de plusieurs ZIP, utilisez `./wikidebia update IDENTIFIANT`. `--archive` et `--scope` restent disponibles pour les cas explicitement particuliers.

La commande `./wikidebia update` sélectionne désormais automatiquement l’unique ZIP présent dans `incoming/`. En présence de plusieurs ZIP, elle exige un identifiant. `--archive` reste accepté à titre de compatibilité. Lorsque `--scope` est omis, la portée est déduite des langues réellement validées et non différées.
