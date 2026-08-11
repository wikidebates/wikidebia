# Migration 2.16.4

Aucune migration de corpus n’est requise. Les ZIP `wikidebia-chatgpt-review-package-1.0` préparés par 2.16.2/2.16.3 restent réimportables lorsque leur provenance locale correspond.

Une revue du graphe rejetée contenant des décisions structurelles explicites peut désormais être appliquée en une commande :

```bash
./wikidebia review-import <debate_id> <zip_revu> --execute-graph-actions
```

Les doublons sont redirigés vers la page conservée ; les retraits non fusionnés peuvent supprimer la page ; déplacements et changements de relation sont pris en charge. Une nouvelle revue du graphe est ensuite générée automatiquement.
