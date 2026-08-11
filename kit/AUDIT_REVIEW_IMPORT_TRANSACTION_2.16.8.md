# Audit — transaction `review-import` 2.16.8

## Invariant

Pour une revue ne déclenchant aucune écriture distante irréversible, l’import et l’avancement mécanique jusqu’au prochain arrêt éditorial forment une transaction logique : soit l’ensemble réussit, soit l’état antérieur reste réimportable.

## Éléments restaurés en cas d’échec

- fichier d’orchestration du débat ;
- base contrôlée de la revue ;
- promotion locale éventuellement créée pendant la tentative ;
- workspace éditorial créé pendant la tentative ;
- artefacts de promotion/release créés pendant la tentative ;
- nouveau paquet `outgoing/` créé pendant la tentative.

## Frontière irréversible

Une action de graphe explicitement exécutée sur le wiki ne peut pas être annulée par un rollback local. Dès qu’un reçu d’écriture distante est acquis, l’état post-action est conservé et sert de point de reprise déterministe.
