# Audit — présence top-level des paramètres éditoriaux historiques — kit 2.16.22

## Anomalie reproduite

Le renderer canonique utilisait la chaîne vide à la fois comme valeur éditoriale vide et comme signal implicite d’omission. Après une revue française de contenu, cela supprimait du wikicode des paramètres pourtant présents historiquement, notamment `A0021 |objections=`, ainsi que les buckets Débat `bibliographie-pour` et `vidéographie-contre` devenus vides. Le préflight les classait alors comme `unauthorized_parameter_deletions`.

## Correctif

- `wikidebia_content_review.py` capture `source_parameter_presence` pour les paramètres éditoriaux gérés des pages françaises préexistantes.
- La présence est propagée sans modifier la valeur éditoriale finale.
- `wikidebia_render.py` distingue trois états : `None` = omission, sentinel `present-empty` = émission `|paramètre=`, valeur non vide = émission normale.
- Le sentinel n’est produit que si la page est `preexisting` et que la présence historique exacte du paramètre est attestée. Un ancien artefact sans cette preuve conserve le comportement prudent d’omission au lieu d’inventer un paramètre.
- Les pages nouvelles suivent le profil de génération courant.
- Les suppressions explicitement autorisées restent indépendantes et continuent d’être traitées par `allowed_parameter_deletions`.

## Régressions

Les tests couvrent A0021, les deux buckets documentaires du Débat, l’absence historique, les valeurs historiques non vides, la suppression autorisée, la propagation import → verrou → checkpoint → handoff anglais, et un préflight de 100 opérations `update` avec zéro `blocked` et zéro `manual_review`.
