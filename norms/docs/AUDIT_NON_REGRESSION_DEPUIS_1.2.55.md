# Audit de non-régression depuis 1.2.55

Base de comparaison : norme 1.2.55, validateur 0.4.58 et kit 2.15.32 fournis au début du cycle de modification.

La révision 1.2.61 conserve toutes les exigences et tous les alias de provenance du paquet initial. Elle restaure en outre l'archive exacte de la norme consolidée 1.2.55 et impose que les futures normes consolidées remplacées soient archivées avant substitution.

Les contrôles différentiels ont révélé et corrigé trois défauts d'intégration : décalage entre les versions de schémas émises par le kit et admises par le validateur, contraintes de portée de `name=` appliquées à tort aux résultats `none`, et validation pré-rendu des revues `name=` fondée exclusivement sur `manifest.pages` alors que celui-ci n'est pas encore peuplé.

La validation finale doit inclure un test croisé kit↔validateur exécuté isolément et une vérification sur extraction fraîche de l'archive exacte.
