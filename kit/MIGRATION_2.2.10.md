# Migration du kit 2.2.10

Le kit 2.2.10 rend la reprise d’un débat entièrement non interactive. La commande `./wikidebia update IDENTIFIANT` planifie la reprise, vérifie l’absence d’opération bloquée, puis transmet automatiquement l’empreinte du plan signé au moteur d’exécution.

L’option historique `--yes` reste acceptée pour ne pas casser les scripts existants, mais elle n’est plus nécessaire et n’a aucun effet. Les protections contre les modifications humaines, les collisions de révision, les droits insuffisants, les suppressions non sûres et les plans altérés restent inchangées.
