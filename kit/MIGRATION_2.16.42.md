# Migration vers le kit 2.16.42

Un Work déjà bloqué en `final_publication` peut provenir d’un ancien état d’orchestration où le checkpoint français de contenu a bien été publié mais où `workflow.json` n’a jamais copié `receipt_sha256` ni `plan_sha256`.

Le kit 2.16.42 peut rattacher ce workflow au reçu courant uniquement si toutes les preuves suivantes concordent : même `debate_id`, même `work_id`, stage `content`, reçu auto-signé et publié, absence d’autorisation/reçu de publication finale, absence d’état anglais signé et `plan_sha256` du reçu identique à celui de `.state/published/<debate>/fr/latest.json`.

Si un ancien `receipt_sha256` est déjà présent sans `plan_sha256`, l’adoption reste refusée : le plan de l’ancien reçu n’est alors pas prouvable. Toute divergence réelle de plan reste bloquante.
