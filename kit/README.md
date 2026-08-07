# Wikidéb’IA — Kit 2.15.31

Le kit 2.15.31 applique l’architecture cumulative 1.2.54 tout en conservant la traduction anglaise 1.2.53 par lots : page Debate en lot autonome, puis lots Argument de 20 pages par défaut (25 maximum, 10–15 lorsque la documentation ou les citations sont denses), avec passe globale inter-lots avant finalisation.

La phase anglaise recherche séparément les appellations consacrées dans la littérature anglophone et n'obtient jamais `name=` par traduction mécanique de `nom=`. Les références françaises ne sont pas traduites : une version anglaise réelle doit être trouvée et citée avec ses propres métadonnées, et de nouvelles références anglophones sont recherchées indépendamment. Le contrat `Citation`→`Quote` reste inchangé : seules les valeurs `quote` et `date` sont traduites et `Citation traduite par IA` est ajouté.

La reprise distante applique cette exception uniquement à `nom` / `name`. Tous les autres paramètres historiques protégés conservent les garanties de la révision 2.15.27.

Correctif actif de traduction : le contenu d'une éventuelle page anglaise cible existante est ignoré pendant la production éditoriale ; les valeurs françaises de progression et d'avertissement sont traduites selon la table officielle sans défaut de création ; `related-debates` ne reprend que les relations françaises dont la page anglaise existe ; chaque lot reçoit une seconde passe FR→EN.

Kit aligné sur la norme 1.2.54 et le validateur 0.4.57.

Les numéros de norme et les anciens champs de révision ne sont plus des feature flags éditoriaux ; ils servent uniquement à la compatibilité technique et à la traçabilité.
