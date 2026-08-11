# Audit de régression kit 2.16.5

Le correctif est limité au chemin de vérification post-écriture des actions de graphe. Les protections de préflight, `baserevid`, identité, droits, balise `chatgpt`, validation prospective et ordre update → redirect → delete sont conservées.

Régressions ajoutées :
- révision temporairement invisible puis visible ;
- balise temporairement absente puis visible ;
- reprise d’une exécution partielle sans seconde écriture de la page déjà conforme.
