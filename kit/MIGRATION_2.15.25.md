# Migration vers le kit 2.15.25

Cette version ajoute l’adoption contrôlée de révisions manuelles distantes. Un corpus peut déclarer la politique 1.2.48 et un registre qui verrouille le titre, la révision, l’empreinte et les éventuels paramètres de cycle de vie autorisés. Sans ce registre, le comportement antérieur `manual_review`/`blocked` reste inchangé.
