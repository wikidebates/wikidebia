# Guide de publication et de reprise Wikidéb’IA 2.2.9

## Nouveau débat

Déposer le ZIP du corpus dans `incoming/`, puis lancer `./wikidebia publish [SÉLECTEUR] --scope all`.

## Débat déjà publié

Installer le corpus puis lancer `./wikidebia update <debate_id> --dry-run`, examiner le plan et exécuter la reprise. Le résumé MediaWiki par défaut est « Corrections ».

## Mise à niveau des composants

Un seul fichier suffit. Vider `updates/`, y copier soit le bundle `WIKIDEBIA_SOURCES_COMPLETES_*.zip`, soit la livraison complète `WIKIDEBIA_LIVRAISON_*.zip`, puis lancer `./wikidebia upgrade`. Les livraisons complètes contiennent les trois composants à leur racine pour les anciens gestionnaires ; le gestionnaire courant sait aussi les retrouver dans un bundle interne.
