# Migration vers le kit 2.7.0

Le kit 2.7.0 ajoute la finalisation et l’application contrôlée de la revue française des titres, rubriques et mots-clés dans un workspace éditorial.

Aucune modification de la norme 1.2.26 ni du validateur 0.4.28 n’est requise. Les fonctions de publication et de reprise distante restent inchangées.

Nouvelles commandes :

```bash
./wikidebia corpus-workspace-review <debate_id> --work-id <work_id> --finalize
./wikidebia corpus-workspace-review <debate_id> --work-id <work_id> --apply --confirm-review-sha256 <empreinte>
```

La phase conserve `working-copy/` comme instantané intact et crée séparément `reviewed-copy/`. Elle ne génère aucune page finale et ne commence aucune traduction anglaise.
