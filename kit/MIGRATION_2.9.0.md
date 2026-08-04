# Migration vers le kit 2.9.0

Le kit 2.9.0 ajoute la traduction anglaise contrôlée après le verrouillage complet du corpus français produit par le kit 2.8.0.

La nouvelle commande est :

```bash
./wikidebia corpus-workspace-translation <debate_id> --work-id <work_id> --prepare|--finalize|--apply
```

Aucune migration destructive n’est effectuée. Les workspaces antérieurs restent utilisables. La phase crée uniquement de nouveaux registres de traduction et, après confirmation de l’empreinte scellée, une `translated-copy/` distincte. Les pages MediaWiki finales ne sont pas encore générées.
