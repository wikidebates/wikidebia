# Wikidéb’IA Validator 0.4.64

La version 0.4.64 applique la norme 1.2.60. Elle conserve sans modification la migration `nom-consacré` / `established-name` de 0.4.62 et confirme que `initialization` reste interdit sur une nouvelle page `Argument` anglaise générée. La fixation de `creation-date` au jour réel de publication relève du moteur de publication signé : le validateur local contrôle la structure du paquet, tandis que le kit remplace cette métadonnée juste avant la création distante.

La version 0.4.62 aligne le validateur sur la norme 1.2.58 : le deuxième paramètre top-level du modèle `Argument` est désormais `nom-consacré` en français et `established-name` en anglais. Les alias historiques `nom` / `name` restent acceptés uniquement pour la lecture et la préservation exacte de pages ou paquets antérieurs attestés ; ils sont refusés sur une nouvelle page relevant du contrat 1.2.58.

Le validateur distingue explicitement ce paramètre MediaWiki des titres de pages, noms de sites, auteurs et champs JSON génériques `name`. Il conserve aussi les contrôles 1.2.57, dont `AI-translated quote`, les conventions de résumé MediaWiki et la double balise de création appliquée par le kit.

Les normes éditoriales courantes sont cumulatives : `consolidated_norm` et les anciens champs `*_revision` ne servent pas de feature flags éditoriaux. La distinction pré-1.2.58 utilisée ici est uniquement une compatibilité de format pour lire et restaurer l’ancien nom de paramètre.
