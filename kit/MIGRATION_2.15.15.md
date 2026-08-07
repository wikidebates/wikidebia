# Migration vers le kit 2.15.15

Le kit reste aligné sur la norme 1.2.39 et exige le validateur 0.4.42. La correction renforce la vérification des verrous historiques : lorsqu’un corpus déclare `verification_revision=0.4.42`, le verrou est confronté à l’inventaire source dont le chemin et l’empreinte sont enregistrés dans le manifeste.
