# Migration vers le kit 2.15.0

Le kit 2.15.0 ajoute la clôture formelle du Work après une exécution distante réussie. Aucun plan 2.14.0 n’est automatiquement clôturé : après la mise à niveau, les preuves doivent être reconstruites avec le kit actif lorsque leur version est engagée dans les empreintes.

La nouvelle commande est `corpus-workspace-close`. Elle exige le SHA-256 exact du reçu d’exécution 2.15.0, vérifie les états publiés et refuse les suppressions différées. Elle archive l’ancien corpus et les preuves avant d’inscrire le Work comme terminé.
