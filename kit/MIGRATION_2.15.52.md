# Migration 2.15.52

Durcissement de preuve aligné sur 1.2.68 / 0.4.71. Le reçu courant de convergence passe à 1.1 avec une `method_family` normalisée et deux familles finales distinctes. Un test négatif explicite empêche l’injection d’un `established-name=` comme keyword, et le parseur de publication possède une fixture multiligne avec sous-modèles imbriqués. Aucun comportement éditorial de 2.15.51 n’est retiré.
