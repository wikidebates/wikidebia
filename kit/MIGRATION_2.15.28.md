# Migration 2.15.28

Cette révision ajoute une exception éditoriale fermée au contrat de préservation : un `nom` / `name` historiquement absent peut être ajouté uniquement si le manifeste active `argument_name_assignment_revision=1.2.51` et référence un registre approuvé par le propriétaire. Sans ce registre, le comportement 2.15.27 reste inchangé.
