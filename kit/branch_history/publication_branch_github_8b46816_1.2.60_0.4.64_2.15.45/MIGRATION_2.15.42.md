# Migration 2.15.42

Maintenance de non-régression sans changement de norme ni de validateur.

`tag-translated-fr` conservait bien, au stade du plan, la compatibilité avec les résumés historiques `Translation of the French page [[:fr:X|X]]`, mais l’exécution 2.15.41 comparait encore la révision au seul nouveau résumé 1.2.57 avec deux-points. Le plan et l’exécution appliquent désormais la même règle : seules les deux formes explicitement autorisées (historique et courante) sont admises, recalculées depuis le titre français source, sans faire confiance à une liste arbitraire du plan.

La maintenance corrige aussi la documentation de provenance : les sections historiques 1.2.56 conservent la forme sans deux-points, la mention `Quote translated by AI` reste attribuée à 1.2.53 comme historique puis explicitement remplacée par `AI-translated quote` en 1.2.57, et le README des normes annonce les versions recommandées actuelles.
