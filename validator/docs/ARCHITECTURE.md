# Architecture du validateur 0.4.16

Le validateur sépare le schéma, la cohérence du registre et du graphe, les fichiers, les lots, les sources, le wikicode, le bilinguisme, l’éditorial et le workflow.

Les contrôles 1.2.11 restent actifs sous 1.2.15, notamment le refus d’une frontière de modèles écrite avec un espace ou un retour à la ligne entre `}}` et `{{`. Le code `WDV-MWK-018` impose la forme `}}{{`.

Les contrôles 1.2.10 sur les références directes, les dates documentaires, les paramètres documentaires, les acronymes et la publication française indépendante restent actifs.

Le moteur résout les chemins en mémoire pour accéder aux fichiers, mais les rapports texte et JSON n’enregistrent jamais le chemin absolu de l’installation. Un argument relatif reste relatif ; un argument absolu extérieur au dossier courant est réduit au nom du paquet.
