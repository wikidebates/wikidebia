# Audit 1.2.86 — provenance éditoriale et reprise différentielle

Statut : **PASSED**.

La révision distingue le cycle de vie de la page cible (`page_origin`) de la provenance éditoriale de la source française (`source_page_origin`). Les quotas et préférences de génération suivent la provenance de la source ou du champ ; les invariants structurels, la qualité intrinsèque, la documentation et la fidélité FR→EN restent applicables selon leur nature.

Contrôles de non-régression couverts : titres affichés historiques nominaux/contextuels sans réécriture propositionnelle ; keywords historiques hors quota mais soumis à atomicité/forme/longueur/vocabulaire ; correction ou décomposition tracée d’un mauvais keyword historique ; jeux historiques dominants >25 % non bloquants ; rubriques historiques >4 conservées et correction de classification justifiée ; suppression de la troncature `[:4]` à l’import ; tri alphabétique français accent-insensible ; résumé historique hors ratio 0,60–1,45 avec revue explicite ; introduction anglaise historique sans obligation `Stakes of the debate`, mais avec adaptation autonome du contexte franco-français et contrôles documentaires intrinsèques.

La norme 1.2.85 originale est conservée immuablement dans `history/WIKIDEBIA_NORME_CONSOLIDEE_1.2.85.md` avec son SHA-256 historique `06b01a271a3f15e23ee6c5d3b2734436034f6e46337e64f7140a4869d879fb16`.
