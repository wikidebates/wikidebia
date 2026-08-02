# Migration vers la norme 1.2.25

Cette migration ne change aucun contenu de débat. Elle met à niveau le protocole de reprise distante et la livraison des composants. Les installations doivent adopter le kit 2.2.12 et le validateur 0.4.27.

Les scripts locaux ou intégrations qui exécutaient un plan contenant `manual_review` doivent désormais traiter ce statut comme bloquant. Les appels utilisant implicitement une archive homonyme doivent employer `--archive SÉLECTEUR`. Les dry-runs peuvent laisser une copie de staging pour audit, mais ne modifient jamais `corpus/`.
