# Audit — publication française avant traduction 1.2.80

Décision propriétaire : les corrections françaises deviennent publiables dès que la revue française complète est validée. La traduction anglaise ne doit pas être préparée sur un état français uniquement local.

Le contrat retenu rend un checkpoint FR `translation_status.en=deferred`, sans `interlangue`, puis réutilise le plan de reprise distante et le contrat `page_specific_v1`. La publication doit produire un reçu avant la préparation anglaise et toute reprise après interruption réutilise le même plan.

Le réimport des paquets de revue est déplacé vers `incoming/` et la sélection porte sur le `debate_id` interne. La validation de `document_kind` est remontée au registre `sources_working.json`.
