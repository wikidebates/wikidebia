# Migration vers le kit 2.15.8

Le kit 2.15.8 s’aligne sur la norme 1.2.33 et le validateur 0.4.35.

- les imports de pages existantes enregistrent `page_origin=preexisting` et l’état exact des paramètres protégés ;
- les pages nouvelles utilisent `page_origin=new` et ne déclarent aucun état préservé ;
- le rendu ajoute les valeurs d’avancement et d’avertissement IA uniquement aux pages nouvelles ;
- les paramètres existants d’avancement, d’avertissement et de débats connexes sont conservés exactement ;
- une source d’Argument est sélectionnée parce qu’elle développe l’argument ; le traitement simultané d’objections est admis ;
- les plans distants bloquent toute modification de ces paramètres protégés, y compris pendant un renommage.

Les workspaces 2.15.7 doivent être régénérés depuis leurs imports afin de produire les nouveaux instantanés de cycle de vie.
