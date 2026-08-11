# Wikidéb’IA Validator 0.4.80

Le validateur 0.4.80 s’aligne sur la norme 1.2.77 et le kit 2.16.6. Il conserve tous les contrôles existants et sert aussi à valider prospectivement le corpus reconstruit avant toute exécution distante d’une décision structurelle de revue.

## Notes héritées du paquet parent 0.4.73

Socle hérité de 0.4.73, ensuite complété par les révisions suivantes.

Elle conserve les contrôles différentiels et sémantiques de la lignée traduction 0.4.64 et intègre les contrôles de la lignée publication GitHub : `nom-consacré` / `established-name`, `AI-translated quote`, absence d'`initialization` sur une nouvelle traduction anglaise, cohérence normative et préservation historique des alias.

Les heuristiques sémantiques restent des signaux de revue humaine ; elles ne réécrivent jamais automatiquement le contenu. Les règles éditoriales actives restent cumulatives et ne sont pas conditionnées par le seul numéro de norme.

Le correctif 0.4.67 ne retire aucun contrôle de 0.4.66 ; il rétablit la continuité des révisions normatives compatibles et ajoute le test de non-régression correspondant.

Le correctif 0.4.69 aligne les diagnostics et la copie normative sur les documents actifs resynchronisés de 1.2.66.

Le correctif 0.4.70 accepte et contrôle les schémas sémantiques 1.4 / 1.3, les changements idiomatiques explicitement revus, le corpus réel de régressions et les preuves de champ scellées.

Le correctif 0.4.71 formalise les familles de méthodes de convergence 1.1 tout en conservant la lecture 1.0.

Le validateur 0.4.72 implémente le renommage des paramètres MediaWiki de la norme 1.2.69 avec compatibilité de lecture historique.

Le correctif 0.4.73 aligne l’exécution du validateur sur les règles déjà actives de première publication anglaise : pas de projection de `initialization` et aucune égalité imposée entre `creation-date` anglaise et `date-création` française.

## Architecture de compatibilité 2026-08-10

Les numéros de release sont une provenance. La compatibilité opérationnelle est pilotée par `CAPABILITIES.json` et les identifiants/version de schéma ; les égalités exactes sont réservées à l’installation, l’anti-downgrade, la reproductibilité et l’audit.
