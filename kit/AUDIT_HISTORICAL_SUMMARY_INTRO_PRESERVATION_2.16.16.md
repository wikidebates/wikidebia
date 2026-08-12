# Audit — préservation des résumés et de l’introduction historiques — 2.16.16

Régression couverte : une reprise réelle du débat « Un revenu de base doit-il être instauré ? » a publié des résumés réécrits, des résumés nouvellement créés sur des pages historiquement sans résumé et une nouvelle introduction. Une restauration distante a été nécessaire.

Garde-fous :
- `prepare`: `keep` + copie exacte ;
- `finalize`: divergence interdite ;
- `apply`: provenance et SHA-256 dans `fr_content_lock.json` ;
- changeset : aucun delta introduction/résumé historique ;
- instructions ChatGPT : champs historiques en lecture seule ;
- tests : résumé existant, résumé absent, introduction historique, orchestration.
