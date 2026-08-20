# Audit — Debate avant Arguments à la publication finale (2.16.46)

Décision propriétaire : la page anglaise `Debate` doit être créée avant les pages `Argument` lors de la première publication finale.

Le chemin 2.16.45 réordonnait explicitement le plan en sens inverse. 2.16.46 inverse ce tri et ajoute une migration de plan bornée pour les publications déjà autorisées ou partiellement exécutées : les pages déjà créées sont conservées et vérifiées comme `skip`, les créations restantes conservent exactement leur contenu/date, `Debate` est placé avant les Arguments restants, puis préflight et autorisation sont rescellés.

Aucune page existante n’est supprimée, recréée ou redatée.
