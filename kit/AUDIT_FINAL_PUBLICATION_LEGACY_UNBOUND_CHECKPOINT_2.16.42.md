# Audit — checkpoint français historique non lié — kit 2.16.42

Le correctif étend uniquement la migration 2.16.41 aux workflows historiques qui ne portaient aucune empreinte de reçu. La preuve d’adoption repose sur le reçu courant auto-signé du même Work et sur l’état français signé courant attestant le même plan.

Régressions couvertes : adoption d’un workflow sans `receipt_sha256`/`plan_sha256`; refus d’un ancien hash lié mais sans plan; refus lorsque l’état français signé diverge; maintien des refus après autorisation finale ou apparition d’un état anglais.
