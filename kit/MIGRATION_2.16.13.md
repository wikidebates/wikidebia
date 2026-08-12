# Migration 2.16.13

Après mise à niveau, les retours ChatGPT doivent être déposés dans `incoming/`. Utiliser :

```bash
./wikidebia review-import
```

S’il existe plusieurs paquets de revue valides :

```bash
./wikidebia review-import <debate_id>
```

Après validation de la revue française de contenu, le kit publie automatiquement les pages françaises scellées avec un résumé individualisé par page puis prépare la revue anglaise. Les workflows 2.16.12 déjà arrêtés sur la revue anglaise sont repris sans refaire la revue : `workflow` publie d’abord le checkpoint français manquant.
