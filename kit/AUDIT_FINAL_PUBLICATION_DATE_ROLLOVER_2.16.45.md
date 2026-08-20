# Audit — reprise de publication anglaise après changement de jour (2.16.45)

## Incident reproduit

Une publication finale anglaise peut commencer avant minuit dans le fuseau de publication puis rencontrer le jour civil suivant avant la création d'une page restante. `GenericPublisher` bloque correctement avant cette création afin de ne jamais publier une `creation-date` devenue fausse. Jusqu'à 2.16.44, la reprise rechargeait toutefois le même plan signé et ne savait pas produire un successeur audité : elle restait donc bloquée alors que les pages déjà créées étaient exactes et que les pages restantes devaient simplement recevoir le nouveau jour réel.

## Correction

`wikidebia_final_publication` construit désormais un plan anglais successeur lorsque le jour courant est strictement postérieur au `publication_date` du plan interrompu et qu'aucun reçu anglais final n'existe encore.

La transition est bornée :

- une ancienne action `create` déjà exécutée doit devenir `skip` après preuve distante de la révision de création (parent 0, utilisateur attendu, contenu, résumé et balises exacts) ; sa `creation-date` et son empreinte doivent rester celles de l'ancien plan ;
- une ancienne action `create` encore absente reste `create`, avec la nouvelle date civile courante ; son nouveau contenu doit différer de l'ancien contenu planifié uniquement par `creation-date` ;
- une ancienne action `skip` doit rester `skip` avec le même contenu ;
- aucune page, aucun titre, aucun chemin source, aucune balise ni aucun résumé de modification ne peut changer ;
- le préflight et l'autorisation sont rescellés sur le plan successeur avant la reprise ;
- les anciens config/plan/préflight/autorisation sont conservés sous `.state/final-publication/<debate>/<work>/publication-date-rollovers/` avec un reçu de transition auto-signé ;
- en cas d'échec de la reconstruction locale, l'état signé précédent est restauré et aucune écriture distante supplémentaire n'est effectuée.

La même logique est appelée préventivement lors d'une relance le lendemain et immédiatement après le blocage de changement de jour lorsqu'il survient pendant une exécution en cours.

## Invariant éditorial

La norme reste 1.2.87 : la `creation-date` d'une nouvelle page anglaise est le jour civil de sa création distante dans le fuseau de publication. Une page créée le 20 août reste datée `2026-08-20`; une page créée le 21 août reçoit `2026-08-21`. Aucune page déjà créée n'est redatée.
