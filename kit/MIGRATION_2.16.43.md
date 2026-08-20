# Migration vers le kit 2.16.43

Aucune intervention manuelle sur `.state/` n'est requise. Lors de la reprise de `final_publication`, le kit peut remplacer un statut local historique non canonique par le reçu français final courant uniquement lorsque l'entrée du workflow n'est liée à aucun reçu ni plan et que les preuves signées du checkpoint et de l'état français concordent exactement.

La migration est traçable dans `workflow.compatibility_migrations` et ne modifie ni le corpus, ni les revues, ni les convergences, ni les reçus de publication.
