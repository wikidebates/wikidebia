# Migration kit 2.16.0

Cette release ajoute une couche d’orchestration au-dessus des primitives existantes. Aucun workflow avancé n’est supprimé.

Usage normal :

```bash
./wikidebia workflow "Un revenu de base doit-il être instauré ?"
./wikidebia review-import revenu_de_base fichier_corrige.zip
./wikidebia workflow-status revenu_de_base
```

Le workflow s’arrête uniquement aux paquets de revue ChatGPT ou à une erreur bloquante. `outgoing/` est privé et exclu de Git. L’orchestrateur ne publie rien sur MediaWiki ; il s’arrête au corpus `release_ready`.
