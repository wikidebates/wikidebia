# Audit — reprise d'un plan signé après mise à niveau (2.16.47)

Le moteur `RemoteUpdatePlanner` déclare déjà `kit_version` et `required_validator_version` comme métadonnées de provenance ; la compatibilité est gouvernée par le schéma/capacités. `PlanExecutor.verify_plan()` conservait pourtant une égalité stricte avec les versions installées, ce qui bloquait une reprise de publication finale déjà commencée après une mise à niveau, avec `Plan divergent : kit_version` puis potentiellement `required_validator_version`.

2.16.47 retire uniquement ces deux égalités de producteur. Le plan reste obligatoirement auto-signé et confirmé par son SHA-256 ; `plan_version`, `debate_id`, l'empreinte du manifeste courant et l'empreinte exacte de la configuration restent vérifiés avant exécution. Les gardes de révision et de contenu distant restent inchangées avant chaque mutation.

Régressions : un plan signé sous 2.16.45 / 0.4.104 est accepté par 2.16.47 lorsque schéma, manifeste et configuration sont inchangés ; une divergence de manifeste ou de configuration reste bloquante.
