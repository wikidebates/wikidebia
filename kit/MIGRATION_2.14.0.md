# Migration vers le kit 2.14.0

Le kit 2.14.0 ajoute `corpus-workspace-plan-execute`, qui prépare un préflight distant signé puis exécute un plan accepté avec les protections du moteur de reprise existant.

Les plans, comparaisons et acceptations produits avec 2.13.0 doivent être reconstruits après la mise à niveau, car leurs empreintes engagent la version exacte du kit. Le flux recommandé est : nouvelle comparaison, nouvelle revue du plan, préflight d’exécution, puis exécution avec confirmation de l’empreinte du préflight.

Aucune migration silencieuse des preuves 2.13.0 n’est effectuée.
