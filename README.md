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

Pour mettre à jour automatiquement une installation Debian après fusion sur GitHub,
voir [le déploiement depuis Codex Web](deploy/README.md).

Pour publier des corrections françaises explicitement demandées depuis Codex,
sans SSH, voir [le relais de publication Debian](deploy/README_PUBLICATION_FR.md).

La correction de pages existantes préserve leurs résumés d’arguments : ne pas en
ajouter, réécrire ou retirer sans demande utilisateur spécifique. Les permissions
par page et les commentaires d’édition calculés à partir du contenu sont décrits
dans [le périmètre éditorial du relais](deploy/README_PUBLICATION_FR.md#périmètre-des-résumés-et-commentaires-dédition).

## Mise à niveau par bundle unique

Vider les anciens ZIP de `updates/`, y déposer uniquement le bundle complet reçu, puis lancer `./wikidebia upgrade`. Le bundle contient les trois composants et le gestionnaire les extrait automatiquement.
- En cas de validation bloquée, `outgoing/<debate_id>_<rapport>_diagnostic.zip` contient automatiquement la liste exhaustive des erreurs et le contexte minimal à transmettre à ChatGPT.
