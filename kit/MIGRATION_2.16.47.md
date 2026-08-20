# Migration 2.16.47 — reprise d’un plan signé après mise à niveau

Aucune modification manuelle de `.state/` n’est requise. Les plans `wikidebia-remote-update-plan-1.0` déjà signés restent vérifiés par leur SHA-256, leur schéma, le débat, le manifeste et la configuration exacts. Les champs `kit_version` et `required_validator_version` sont conservés comme provenance de la simulation d’origine et ne sont plus comparés au numéro du producteur qui exécute la reprise.

Cette migration vise notamment la publication finale déjà commencée : un plan français scellé avant une mise à niveau peut être exécuté après celle-ci sans être reconstruit seulement pour réécrire des numéros de version. Toute divergence de contenu, de manifeste, de configuration ou de révision distante reste bloquante.
