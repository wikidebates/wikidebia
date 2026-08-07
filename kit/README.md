# Wikidéb’IA — Kit 2.15.26

Le kit 2.15.26 conserve strictement le paramètre historique `nom` des pages `Argument` françaises et `name` des pages anglaises. Il capture son état exact à l’import et le réémet sans modification lors du rendu. Un renommage de page ne modifie jamais ce champ, et une page qui n’en possédait pas n’en reçoit pas artificiellement.

Le registre d’adoption distante 1.2.48, la préservation de `débat-détaillé` / `detailed-debate` et les autres protections de contenu historique restent actives.

Kit de production, publication et reprise aligné sur la norme 1.2.49 et le validateur 0.4.52.

Pour mettre à jour un débat, déposez son ZIP dans `incoming/` puis lancez `./wikidebia update`.
