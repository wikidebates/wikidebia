# Audit — atomicité localisée des mots-clés anglais (2.16.31)

Le correctif conserve les concepts et l’ordre de pertinence validés. Il localise uniquement les attestations formelles dont la valeur dépend de la forme linguistique cible.

- la forme française reste décrite par les champs historiques non préfixés ;
- la forme anglaise reçoit `en_kind`, `en_capitalization_policy`, `en_atomic_concept`, `en_compositional_intersection`, `en_multiword_exception` et `en_multiword_exception_rationale` ;
- une locution française nécessitant une exception peut devenir un composé anglais de deux mots sans exception ;
- une forme anglaise de plus de deux mots ou contenant un connecteur reçoit une exception et une justification propre ;
- `WDV-EDT-025` reste inchangé et continue de bloquer une véritable intersection compositionnelle ou une exception insuffisamment justifiée.

Régressions : tests unitaires et d’application de la traduction, plus vérification sur les 72 équivalents du vocabulaire du vote électronique (zéro faux signal restant).
