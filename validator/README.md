# Wikidéb’IA Validator 0.4.62

La version 0.4.62 aligne le validateur sur la norme 1.2.58 : le deuxième paramètre top-level du modèle `Argument` est désormais `nom-consacré` en français et `established-name` en anglais. Les alias historiques `nom` / `name` restent acceptés uniquement pour la lecture et la préservation exacte de pages ou paquets antérieurs attestés ; ils sont refusés sur une nouvelle page relevant du contrat 1.2.58.

Le validateur distingue explicitement ce paramètre MediaWiki des titres de pages, noms de sites, auteurs et champs JSON génériques `name`. Il conserve aussi les contrôles 1.2.57, dont `AI-translated quote`, les conventions de résumé MediaWiki et la double balise de création appliquée par le kit.

Les normes éditoriales courantes sont cumulatives : `consolidated_norm` et les anciens champs `*_revision` ne servent pas de feature flags éditoriaux. La distinction pré-1.2.58 utilisée ici est uniquement une compatibilité de format pour lire et restaurer l’ancien nom de paramètre.
