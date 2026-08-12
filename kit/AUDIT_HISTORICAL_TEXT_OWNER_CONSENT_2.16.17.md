# Audit — consentement propriétaire pour les textes historiques — 2.16.17

Statut : **PASSED**.

Le correctif remplace l’immutabilité absolue de 2.16.16 par le contrat suivant : préservation par défaut, suggestion possible, consentement propriétaire explicite, delta autorisé et traçable.

Contrôles vérifiés :

- aucune modification historique sans consentement ;
- une suggestion seule reste non publiable ;
- le ZIP éditable ne peut pas fabriquer le reçu de consentement ;
- `review-import --authorize-historical-changes` lie localement le consentement à l’archive exacte, au package/manifeste, aux champs et aux SHA avant/après ;
- consentement multi-champs limité à la portée demandée ;
- correction locale et réécriture substantielle autorisées sans réédition parasite ;
- suppression de `<references />` et ajout de `Enjeux du débat` autorisables dans la revue courante ;
- absence historique de résumé conservée sauf création nominativement autorisée ;
- anciennes revues supportées migrées par schéma/données, sans perte des décisions de classification/documentation ;
- `fr_content_lock.json` distingue `preserved` / `authorized_change` ;
- checkpoint français n°2 publie les deltas autorisés et aucune troisième frontière n’est ajoutée ;
- traduction anglaise fondée sur la version française finale autorisée ;
- suites complètes du kit : 453/453.
