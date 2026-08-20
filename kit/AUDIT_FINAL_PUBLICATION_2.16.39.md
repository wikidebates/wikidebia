# Audit — publication finale automatique 2.16.39

## Objet

Le kit 2.16.39 ferme le dernier écart d’orchestration après un Work éditorial bilingue : un workflow arrivé à `release_ready` ne s’arrête plus avant MediaWiki. Il entre dans `final_publication`, construit toutes les preuves en lecture seule, publie uniquement si le plan complet est sûr, puis installe le `release-copy` comme corpus actif.

## Baseline finale liée au Work

La baseline n’est jamais déduite de la seule absence d’un reçu anglais. Le module `wikidebia_workflow_baseline.py` vérifie conjointement :

- l’identité `debate_id` / `work_id` du `release_ready` exact ;
- l’empreinte du `release-copy` et du reçu de release ;
- le reçu du dernier checkpoint français et `.state/published/<débat>/fr/latest.json` ;
- la concordance du plan français signé avec ce checkpoint ;
- le manifeste installé préalable portant explicitement `translation_status.en=deferred` et aucune page EN ;
- l’absence d’une phase de publication anglaise antérieure dans ce Work ;
- la barrière `publication_started=false` du reçu de release.

La preuve anglaise signifie donc `never_published_by_this_work`. Elle ne signifie jamais « la page distante est absente ». Toute existence distante est relue et classée avant écriture.

## Préflight global avant la première écriture

Trois plans sont produits avant autorisation :

1. plan de sûreté bilingue avec le moteur `RemoteUpdatePlanner` ;
2. plan exact de première publication EN avec `GenericPublisher` ;
3. plan exact FR limité aux ajouts interlangues.

La publication automatique est refusée si le plan comporte `blocked`, `manual_review`, `move`, `redirect` ou `delete`, une création FR, une mise à jour EN, ou une mise à jour FR autre que `french_interlanguage_addition`.

Le préflight relit ensuite toutes les cibles et vérifie les révisions/empreintes, les identités, les droits et les balises `chatgpt` / `translated-fr` avant de créer l’autorisation d’exécution.

## Exécution

- Les pages EN utilisent le moteur de première publication afin de conserver la `creation-date` au jour réel de création, le résumé `Translation of the French page: ...` et les balises `chatgpt` + `translated-fr`.
- Dans cette phase finale, les Arguments EN sont exécutés avant la page Debate.
- Les pages FR sont ensuite mises à jour par le plan signé `RemoteUpdatePlanner`, avec les résumés individualisés d’ajout interlangue et garde de révision.
- Une interruption après autorisation conserve les plans et reçus sous `.state/final-publication/<débat>/<work>/` et reprend idempotemment ; aucune convergence sémantique n’est rouverte.
- Après succès, le `release-copy` exact est installé comme corpus actif avec sauvegarde de l’ancien corpus.

## Compatibilité `update --archive`

`StateResolver` consulte désormais en priorité la baseline Work-scoped lorsqu’un ZIP `release_ready` contient le `reports/release_report.json` du Work correspondant. Le fallback 2.16.38 vers un ancien manifeste explicitement `en=deferred` reste disponible pour les corpus historiques qui ne proviennent pas de ce workflow.

## Non-régression

La modification ne touche aucun contenu éditorial, ne modifie ni les verrous français/anglais ni les reçus de convergence, et ne relance ni rendu ni release pour un Work déjà `release_ready`.
