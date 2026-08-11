# Audit de non-régression 0.4.77

Le validateur 0.4.77 conserve les contrôles du parent 0.4.76 et corrige l’ordre de validation pré-revue. Les contraintes purement éditoriales de forme des titres ne sont plus imposées par le schéma structurel avant le verrou ; les mêmes règles sont appliquées comme avertissements avant verrou puis comme erreurs après verrou. Les erreurs structurelles restent inchangées. Suite complète : 404/404 tests réussis avant scellement ; une nouvelle passe est exécutée sur l’archive fraîche exacte.
