# Audit — rendu différentiel des textes historiques — Validator 0.4.96

## Incident reproduit

Le préflight final du corpus historique `revenu_de_base` bloquait sur quatre anomalies déjà présentes ou attestées dans la source française : `<references />` dans l’introduction, `Sous-partie.avertissements`, un ancien paramètre `infobulle` de `Lien Wikipédia` dans A0011, et l’absence historique de `résumé` dans A0012.

## Cause

Le rendu final appliquait indistinctement des règles de nouvelle génération à des champs historiques pourtant scellés comme préexistants. Le verrou de provenance était disponible mais n’était pas utilisé par les contrôles concernés.

## Correctif

Le kit courant déclare `historical_text_render_validation_mode=differential_preservation_v1`. Le validateur n’active les exceptions de provenance legacy qu’en présence de ce mode. Les textes restent inchangés : le correctif agit uniquement sur la qualification des contrôles. Les pages nouvelles et les textes non attestés restent strictement validés.

## Régressions

`tests/test_historical_render_differential_0496.py` couvre le cas historique positif et le cas nouveau négatif. Les tests historiques de résumé absent et de préservation des textes restent également exécutés.
