# Audit — référence du checkpoint français final — kit 2.16.41

Le correctif ne modifie aucune page ni aucun reçu de publication français. Il répare uniquement la copie périmée du reçu stockée dans `workflow.json` lorsque le reçu courant et l’état publié FR signé attestent le même `plan_sha256`.

Garde-fous :

- même débat et même Work ;
- stage `content` et statut publié/no_changes ;
- même `plan_sha256` entre l’ancienne référence du workflow et le reçu courant ;
- même plan dans `.state/published/<débat>/fr/latest.json` ;
- aucune `authorization.json` ni reçu final ;
- aucun état anglais signé.

Une divergence de plan reste bloquante.
