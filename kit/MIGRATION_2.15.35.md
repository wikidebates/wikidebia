# Migration 2.15.35

Maintenance sans changement de norme ni de validateur. Le kit 2.15.35 corrige la reprise française après publication de la traduction anglaise : l’ajout tardif de `interlangue` est une exception explicite à la préservation de l’absence historique lorsque `translation_status.en` vaut `ready` ou `published`.

Lorsqu’une mise à jour française ne fait qu’ajouter le lien interlangue vers la page anglaise verrouillée, le plan signé reçoit le résumé individualisé exact `Ajout du lien interlangue vers la page anglaise [[en:X|X]]`, où `X` est le titre canonique anglais de la même `page_id` et du même type de page. L’exécuteur recalcule ce résumé, confirme que la modification reste un ajout interlangue pur et relit la révision écrite pour vérifier contenu, résumé et balise `chatgpt`.
