# Migration vers le kit 2.1.15

1. Remplacer le kit 2.1.14 par le kit 2.1.15.
2. Ne pas modifier les champs historiques `normative_versions` du manifeste d’un corpus déjà produit.
3. Le kit exécute le validateur installé 0.4.15 et exige un rapport positif de cette version.
4. Le corpus peut déclarer une norme antérieure explicitement compatible, par exemple 1.2.10, et conserver le validateur qui a servi à sa production, par exemple 0.4.10.
5. La publication reste bloquée si le validateur installé refuse le corpus, si sa version réelle diverge, ou si le plan et les empreintes ne correspondent pas.
