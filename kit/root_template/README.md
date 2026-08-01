# Installation Wikidéb’IA

- `./wikidebia publish [SÉLECTEUR]` : publication initiale ;
- `./wikidebia update IDENTIFIANT [--dry-run|--no-delete|--only-delete]` : reprise distante contrôlée ;
- `./wikidebia upgrade` : mise à niveau des composants depuis un ZIP complet unique de préférence ;
- `./wikidebia doctor` : diagnostic local.

Les secrets Pywikibot résident dans `private/pywikibot/`. Les corpus, plans, reçus, états, journaux et archives ne sont pas versionnés.

## Mise à niveau par bundle unique

Vider les anciens ZIP de `updates/`, y déposer uniquement le bundle complet reçu, puis lancer `./wikidebia upgrade`. Le bundle contient les trois composants et le gestionnaire les extrait automatiquement.
