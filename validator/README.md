# Wikidéb’IA Validator 0.4.85

Le validateur 0.4.85 s’aligne sur la norme 1.2.81 et le kit 2.16.14. Il conserve tous les contrôles de 0.4.84, notamment `WDV-RMT-008`. Les deux checkpoints français utilisent les mêmes schémas de corpus et de plan ; leur séparation fonctionnelle est imposée par l’orchestrateur et ses tests de non-régression.

# Wikidéb’IA Validator 0.4.84

Le validateur 0.4.84 s’aligne sur la norme 1.2.80 et le kit 2.16.13. Il conserve `WDV-RMT-008` pour les résumés MediaWiki individualisés et tous les contrôles antérieurs. Le checkpoint français intermédiaire est validé avec les portées structurelles/documentaires applicables avant la publication distante ; les attestations éditoriales françaises proviennent des verrous déjà scellés.

Le validateur 0.4.83 ajoute le contrôle `WDV-RMT-008` : lorsqu’un plan de reprise déclare le contrat `page_specific_v1`, chaque création, mise à jour, renommage, redirection ou suppression doit porter une politique et un résumé MediaWiki individualisés ; le résumé générique `Corrections` est refusé. Les plans historiques dépourvus de ce contrat restent lisibles.

Le validateur 0.4.82 corrige le contrôle `WDV-EDT-016` : les constructions impersonnelles françaises `Il faut…` et `Il ne faut…` ne constituent pas un référent contextuel. Un véritable pronom anaphorique initial reste bloquant.

Le validateur 0.4.81 distingue désormais les pages `new` des pages `preexisting` pour les règles de création relatives aux titres affichés et au nombre de mots-clés. Une page préexistante peut conserver un titre affiché nominal et un nombre historique de mots-clés ; les autres contrôles de qualité restent actifs.

# Wikidéb’IA Validator 0.4.80

Le validateur 0.4.80 s’aligne sur la norme 1.2.77 et le kit 2.16.8. Il conserve tous les contrôles existants et sert aussi à valider prospectivement le corpus reconstruit avant toute exécution distante d’une décision structurelle de revue.

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
