# Audit documentaire — Kit 2.16.28

La release 2.16.28 réconcilie les deux branches 2.16.27 sans retirer `en_documentation_correction`.

Deux régressions sont couvertes :

- une ressource anglaise déjà présente sous une identité canonique DOI/URL est réutilisée ; le cas DEF CON remappe `S10003` vers `S00013`, conserve la notice historique et ajoute l’usage anglais ;
- un `legal_text` de bibliographie Debate n’est pas rejeté par son seul type lorsque sa portée est `foundational_work` ou `broad_synthesis` et sa sélection est suffisamment justifiée.

Une divergence réelle de `type` ou `document_kind` pour une même identité reste bloquante.
