# Audit de régression kit 2.15.54

Le kit conserve l’écrasement runtime de `creation-date` au jour de publication, le rejet de `initialization` sur une nouvelle traduction anglaise, le contrôle de changement de jour et toutes les capacités 2.15.53. Deux regression gates supplémentaires protègent l’alignement du validateur courant.

Un troisième regression gate protège l’attribution historique des versions 2.15.52/2.15.53 afin qu’un futur bump ne réétiquette pas rétroactivement un changement déjà publié.
