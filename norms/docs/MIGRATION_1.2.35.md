# Migration vers la norme 1.2.35

La révision 1.2.35 est un correctif de compatibilité. Un corpus historique 1.2.x ne doit pas changer sa `normative_versions.consolidated_norm` pour utiliser la traduction anglaise différée. Il ajoute seulement :

```json
"translation_status": {"en": "deferred"}
```

Les corpus importés possédant plusieurs dates de création peuvent en outre déclarer `editorial_controls.creation_date_policy=per_page_preserved`.
