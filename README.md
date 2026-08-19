# Installation Wikidéb’IA

- `./wikidebia graph-extract "TITRE DU DÉBAT"` : extraction récursive en lecture seule ;
- `./wikidebia corpus-init-from-snapshot SNAPSHOT --debate-id IDENTIFIANT` : construction d’un corpus local `graph_draft` ;
- `./wikidebia corpus-review-graph IDENTIFIANT --prepare|--finalize` : revue formelle du graphe ;
- `./wikidebia corpus-promote IDENTIFIANT --confirm-review-sha256 EMPREINTE` : promotion atomique vers `corpus/` ;
- `./wikidebia corpus-workspace-init IDENTIFIANT` : ouverture du workspace éditorial ;
- `./wikidebia corpus-workspace-review IDENTIFIANT --work-id WORK --finalize|--apply` : validation et application contrôlée des métadonnées françaises ;
- `./wikidebia publish [SÉLECTEUR]` : publication initiale ;
- `./wikidebia update IDENTIFIANT [--dry-run|--no-delete|--only-delete]` : reprise distante contrôlée ;
- `./wikidebia upgrade` : mise à niveau des composants depuis un ZIP complet unique de préférence ;
- `./wikidebia doctor` : diagnostic local.

Les secrets Pywikibot résident dans `private/pywikibot/`. Les corpus, plans, reçus, états, journaux et archives ne sont pas versionnés.

## Mise à niveau par bundle unique

Vider les anciens ZIP de `updates/`, y déposer uniquement le bundle complet reçu, puis lancer `./wikidebia upgrade`. Le bundle contient les trois composants et le gestionnaire les extrait automatiquement.
- En cas de validation bloquée, `outgoing/<debate_id>_<rapport>_diagnostic.zip` contient automatiquement la liste exhaustive des erreurs et le contexte minimal à transmettre à ChatGPT.
