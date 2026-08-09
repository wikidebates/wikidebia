# Migration 2.15.36

Maintenance sans changement de norme ni de validateur. Le planificateur de reprise ne s’arrête plus globalement lorsqu’un titre distant existant ne contient pas le modèle principal attendu (`Débat`/`Argument`). La page est isolée dans `manual_review` si elle appartient à l’état publié, ou dans `blocked` si elle n’est pas attestée. Le plan conserve le titre, la révision, l’empreinte, l’erreur structurelle et un extrait du wikicode distant. Aucune de ces opérations ne peut être exécutée tant qu’elle reste non résolue.
