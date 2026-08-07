# Wikidéb’IA Validator 0.4.55

La version 0.4.55 ajoute `WDV-EDT-032`. Pour toute page Argument nouvelle sous la norme 1.2.52, le validateur exige une revue documentaire de l’éventuelle appellation consacrée. Le résultat normal peut être `none`; `nom` / `name` n’est accepté que lorsque la revue conclut `known_name`, fournit une preuve documentaire et correspond exactement au wikicode.
La version 0.4.54 ajoute le contrôle de la politique 1.2.51 d’attribution éditoriale explicite de `nom` / `name`. Une absence historique reste protégée par défaut ; seules les pages listées dans un registre approuvé peuvent recevoir la valeur exacte déclarée.

Validateur local aligné sur la norme 1.2.52 et rétrocompatible avec les paquets antérieurs.
