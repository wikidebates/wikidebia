# Audit — export automatique des diagnostics de validation (2.16.33)

Le kit 2.16.33 généralise le paquet de diagnostic déjà disponible pour la validation initiale à tous les appels du validateur effectués via `_run_validator`.

Lorsqu'une validation échoue, le kit écrit automatiquement dans `outgoing/` un ZIP nommé `<debate_id>_<rapport>_diagnostic.zip`. Il contient la liste exhaustive des erreurs (`ERRORS.json`, `ERRORS.txt`), le rapport JSON/TXT complet, le manifeste du paquet validé, les registres/verrous de contexte utiles disponibles et les fichiers directement pointés par les erreurs.

Le diagnostic est strictement en lecture seule vis-à-vis du corpus validé. Il exclut les secrets et les états d'authentification, impose des limites de taille aux fichiers de contexte et ne peut jamais masquer l'erreur du validateur si sa propre création échoue.

Deux régressions vérifient qu'un rapport contenant plus de quatre erreurs exporte bien l'ensemble des erreurs dans le ZIP et qu'une panne de génération du diagnostic laisse le blocage original intact.
