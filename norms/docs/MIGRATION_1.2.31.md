# Migration vers la norme 1.2.31

La révision 1.2.31 introduit deux décisions :

- les mots-clés sont classés par pertinence décroissante, du plus direct au moins direct ;
- la profondeur du graphe est non limitée et ne produit aucun avertissement de seuil.

Les corpus 1.2.30 restent validables sous leur contrat historique. Une migration vers 1.2.31 remplace `depth_policy.normal_target`, `declared_maximum` et `exception_reason` par `limit_policy: unbounded`, puis ajoute les attestations de classement des mots-clés dans les revues française et anglaise.
