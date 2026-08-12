# Audit 1.2.83 — préservation des résumés et de l’introduction historiques

Régression couverte : lors d’une reprise réelle du débat sur le revenu de base, `fr_content_review` avait réécrit des résumés historiques, créé des résumés là où ils étaient historiquement absents et remplacé l’introduction du débat. Ces modifications ont nécessité une restauration distante.

Garde-fous 1.2.83 :
- contenu historique marqué `preexisting` en lecture seule pour introduction/résumés ;
- absence historique de résumé conservée ;
- verrou SHA-256 avant rendu ;
- delta intro/résumé interdit au checkpoint de contenu ordinaire ;
- nouvelle écriture possible seulement par opération corrective distincte explicitement autorisée.
