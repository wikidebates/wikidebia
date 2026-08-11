# Migration 2.16.1

Aucune migration de corpus n’est requise. Les workflows 2.16.0 déjà bloqués sur `initial_validation_blocked` sont repris par simple relance de `./wikidebia workflow ...` après mise à niveau. Les paquets de revue `wikidebia-chatgpt-review-package-1.0` restent compatibles.

Le validateur 0.4.77 reporte comme avertissements, avant verrou de métadonnées, les défauts éditoriaux de titres qui seront traités à la revue suivante. Les erreurs structurelles restent bloquantes.
