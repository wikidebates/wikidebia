# Audit de complétude 1.2.49

La révision 1.2.49 traite `nom` / `name` comme un paramètre historique protégé de page Argument. La règle est présente dans la norme consolidée, les schémas du verrou historique, le validateur, le kit d’import et de rendu, ainsi que les tests de non-régression. La présence comme l’absence historique sont préservées afin d’empêcher aussi bien une suppression qu’une invention silencieuse.
