# Migration vers le kit 2.15.24

Cette version conserve les paramètres historiques `débat-détaillé` et `detailed-debate`. Une frontière de graphe peut arrêter le parcours sans effacer ce paramètre. Les relations locales ne sont omises que si le verrou historique indique `relations_omitted=true` et `owner_notified=true`.
