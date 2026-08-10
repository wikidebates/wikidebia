# Migration 2.15.35

Le kit 2.15.35 applique la norme 1.2.58 et le validateur 0.4.61. Les paquets de traduction nouveaux ou réappliqués génèrent `data/documentary_resources.json` et déclarent `semantic_marker_engine_version=1.0`. Le reçu externe de release expose quatre couches de validation. Les anciens corpus restent lisibles; ne pas fabriquer rétroactivement un registre de recherche humaine absent, mais le registre documentaire global peut être régénéré déterministement depuis `sources.json`.
