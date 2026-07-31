# Migration vers la norme 1.2.3

1. Déclarer `consolidated_norm=1.2.3`, le validateur 0.4.3 et le kit 2.1.3.
2. Régénérer les manifestes et empreintes.
3. Exécuter toutes les portées du validateur.
4. Produire le plan signé de publication.
5. Vérifier que l’unique page Débat française est classée absente.
6. Exécuter le mode `debate-test`, qui crée cette page canonique avec `createonly` et produit son reçu.
7. Publier les autres pages avec le même plan et le reçu de test de la page Débat.
8. Ne créer aucune sous-page utilisateur de test.

Une page Débat française déjà existante bloque ce workflow et exige une décision explicite de reprise ; elle ne peut pas être écrasée automatiquement.
