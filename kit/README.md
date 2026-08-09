# Wikidéb’IA — Kit 2.15.44

Le kit 2.15.44 applique la norme 1.2.59. La page Debate reste un lot autonome ; les Arguments sont relus en unités internes de 10 pages par défaut, réduites à 5–8 pour les groupes denses. Une livraison Work peut agréger plusieurs unités déjà closes sans transformer les exemples ou checklists en patrons mécaniques.

La phase anglaise recherche séparément les appellations consacrées dans la littérature anglophone et n'obtient jamais `established-name=` par traduction mécanique de `nom-consacré=`. Elle compare les formes concurrentes sans normaliser artificiellement `Argument from X`, `X argument` ou les possessifs, et refuse un nom dont la portée est plus étroite que celle de la page. Les références françaises ne sont pas traduites : une version anglaise réelle doit être trouvée et citée avec ses propres métadonnées, et de nouvelles références anglophones sont recherchées indépendamment. Le contrat `Citation`→`Quote` reste inchangé : seules les valeurs `quote` et `date` sont traduites et `AI-translated quote` est ajouté.

La reprise distante applique cette exception à l’appellation consacrée : `nom-consacré` / `established-name` pour les nouvelles attributions, avec `nom` / `name` uniquement comme alias de préservation historique attestée. Tous les autres paramètres historiques protégés conservent les garanties de la révision 2.15.27.

Correctif actif de traduction : le contenu d'une éventuelle page anglaise cible existante est ignoré pendant la production éditoriale ; les valeurs françaises de progression et d'avertissement sont traduites selon la table officielle sans défaut de création ; `related-debates` ne reprend que les relations françaises dont la page anglaise existe ; chaque lot reçoit une seconde passe FR→EN.

Kit aligné sur la norme 1.2.59 et le validateur 0.4.63.

Lorsqu'un résumé français est historiquement absent et attesté, le workflow anglais conserve cette absence et n'exige aucun `summary=` de remplacement.

Les numéros de norme et les anciens champs de révision ne sont plus des feature flags éditoriaux ; ils servent uniquement à la compatibilité technique et à la traçabilité.

## Rattrapage de la balise de traduction

Pour une traduction anglaise déjà publiée sans la seconde balise, utiliser `./wikidebia tag-translated-fr DEBAT --dry-run`, puis `./wikidebia tag-translated-fr DEBAT`. Le rattrapage cible les révisions de création attestées et n’altère ni le wikicode ni le résumé de modification.

Les futures créations anglaises issues d’une traduction française reçoivent automatiquement les deux balises `chatgpt` et `translated-fr`.
