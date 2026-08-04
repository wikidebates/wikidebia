# Migration vers le kit 2.12.0

Le kit 2.12.0 ajoute `corpus-workspace-remote-compare`. La commande consomme une `release-copy/` scellée, construit une base historique explicite, lit les pages distantes sans aucun appel d’écriture, produit un inventaire observé, un plan signé et un reçu de comparaison.

Les plans restent compatibles avec le schéma de reprise distante 1.0 et le validateur 0.4.29. Aucun plan n’est exécuté par cette commande.
