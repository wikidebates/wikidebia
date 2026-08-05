# Migration vers la norme 1.2.38

La révision 1.2.38 remplace les pseudo-simplifications adjectivales par une décomposition sémantique. Une intersection transparente de domaines est séparée en unités de navigation : `psychologie religieuse` devient `psychologie`, `religion`; `science et religion` devient `science`, `religion`.

Une locution conventionnelle irréductible reste entière. `argument d'autorité` demeure donc un mot-clé atomique, comme `problème du mal` ou `charge de la preuve`.

Chaque entrée du vocabulaire porte `atomic_concept`, `compositional_intersection`, `multiword_exception` et, lorsque cette dernière vaut `true`, une justification propre à la locution. Les revues de résumés portent `originality_reviewed` et `mechanism_statement`.
