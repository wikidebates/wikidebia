# Migration du kit 2.2.4

Le kit 2.2.4 est une maintenance de non-régression. Il conserve le bundle complet unique de 2.2.3 et toutes les fonctions de publication et de reprise.

- aucune modification de corpus n’est requise ;
- le bundle complet reste le seul fichier recommandé dans `updates/` ;
- `./wikidebia upgrade` met les composants à niveau ;
- `./wikidebia update IDENTIFIANT` reprend un débat déjà publié ;
- `./wikidebia publish` reste non interactif ;
- les précontrôles Wikipédia, débats connexes et auteurs restent bloquants.
