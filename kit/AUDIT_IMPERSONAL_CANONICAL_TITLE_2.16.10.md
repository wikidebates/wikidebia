# Audit — titre canonique impersonnel 1.2.78 / 0.4.82 / 2.16.10

Anomalie reproduite : `WDV-EDT-016` signalait à tort `Il ne faut pas instaurer plus de temps libre` comme dépendant d’un contexte extérieur.

Cause : l’exception grammaticale couvrait `Il faut…` mais pas sa négation `Il ne faut…`.

Correction : l’exception reconnaît désormais `(?:ne )?faut` après `Il`.

Régressions vérifiées :
- `Il faut instaurer un revenu de base` : aucun signal contextuel ;
- `Il ne faut pas instaurer plus de temps libre` : aucun signal contextuel ;
- `Il réduit la liberté individuelle` : `initial_contextual_referent` demeure détecté.

Aucune règle d’autonomie du titre canonique n’est assouplie.
