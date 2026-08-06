# Migration 2.15.17

`./wikidebia update` sélectionne désormais l’unique ZIP de `incoming/` sans exiger `--archive`. En présence de plusieurs ZIP, utilisez `./wikidebia update IDENTIFIANT`. Sans ZIP entrant, la commande utilise le corpus installé non ambigu.

Lorsque `--scope` est omis, le kit choisit automatiquement les langues publiables : `fr` pour un corpus dont l’anglais est différé, `all` lorsque les deux langues sont validées. Une portée explicite reste prioritaire.
