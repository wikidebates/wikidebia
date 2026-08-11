# Audit de régression kit 2.16.7

Base vérifiée : 1.2.77 / 0.4.80 / 2.16.6.

Incident reproduit : deux vagues successives de correction du graphe, la seconde écrasant `reviews/graph_action_decisions.json`, tandis qu’un fichier modifié par la première vague conserve l’ancien `sha256` de provenance 2.16.5. La 2.16.6 ne pouvait plus attester cette première mutation et bloquait sur `Empreinte de provenance divergente`.

Correctif :
- lecture additionnelle des historiques immuables `.state/graph-actions/<débat>/*/plan.json` et `execution-receipt.json` ;
- validation des schémas, du débat, de `plan_sha256`, de `receipt_sha256` et du lien reçu→plan ;
- correspondance stricte du contenu courant avec `desired_sha256` et de la révision locale avec la révision écrite attestée ;
- aucun élargissement à une dérive non attestée.

Non-régression : 414/414 tests du kit passent, dont la nouvelle régression multi-vagues ; norme 1.2.77 et validateur 0.4.80 inchangés.
