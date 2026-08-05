# Migration vers le kit 2.15.6

Le kit 2.15.6 s’aligne sur la norme 1.2.31 et le validateur 0.4.33.

- `corpus-init-from-snapshot` génère une politique de profondeur non limitée ;
- la revue française exige un ordre de mots-clés par pertinence décroissante ;
- la revue anglaise conserve exactement ce classement ;
- aucune alerte n’est déclenchée à partir d’un niveau ou d’une profondeur numérique.

Les workspaces 1.2.27 à 1.2.30 restent migrables par les chemins de compatibilité existants.
