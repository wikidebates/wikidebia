# Migration vers le kit 2.15.2

Le kit 2.15.2 corrige le rendu anglais des citations : `quotes=` contient `{{Quote}}`, tandis que la page française conserve `{{Citation}}`. Les paramètres verrouillés ne sont pas renommés ; seules les valeurs de `citation` et de `date` sont traduites.

Les `rendered-copy/`, `release-copy/`, plans ou preuves engageant 1.2.28 / 2.15.1 doivent être reconstruits avant exécution distante. Toutes les commandes et protections du bundle source 2.4.0 restent présentes.
