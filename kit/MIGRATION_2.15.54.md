# Migration kit 2.15.54

Aucun changement du moteur de publication : ses garde-fous `initialization` et `creation-date` étaient déjà corrects. Cette version accompagne le validateur 0.4.73 et ajoute des regression gates inter-composants garantissant que le validateur ne contredit plus ces règles.

Le correctif restaure aussi l’attribution historique exacte des entrées 2.15.52 (durcissement des preuves) et 2.15.53 (renommage des paramètres), qui avaient été fusionnées sous le seul numéro 2.15.53 dans la documentation active du parent.
