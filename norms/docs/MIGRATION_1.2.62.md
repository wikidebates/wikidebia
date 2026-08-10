# Migration 1.2.62 — réconciliation des branches traduction et publication

Cette révision fusionne deux lignées issues de 1.2.55 / 0.4.58 / 2.15.32 :

- traduction/validation : 1.2.61 / 0.4.64 / 2.15.38 ;
- publication GitHub : commit `8b46816`, 1.2.60 / 0.4.64 / 2.15.45.

Aucune histoire n'est réécrite. Les migrations concurrentes portant les mêmes numéros sont archivées sous des chemins qualifiés par branche. Les exigences publication qui entraient en collision avec des identifiants déjà utilisés par la lignée traduction reçoivent de nouveaux identifiants : `TRN-019` pour l'absence d'`initialization` sur une nouvelle traduction anglaise et `RND-009` pour la date réelle de publication. `PUB-045` à `PUB-047` sont conservées.

La réconciliation rend simultanément actives :

- les règles de traduction différentielle, de revue sémantique, de documentation, de portée des appellations consacrées et de scellement d'archive de 1.2.61 ;
- les conventions de publication FR→EN de la branche GitHub : résumé individualisé, balises `chatgpt` + `translated-fr`, ajout interlangue signé, `nom-consacré` / `established-name`, `AI-translated quote`, absence d'`initialization` sur une nouvelle page anglaise et `creation-date` au jour réel de publication.

Les pages déjà publiées ne sont pas réécrites automatiquement.
