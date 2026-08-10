# Audit de non-régression — Validateur 0.4.72

Le validateur 0.4.72 implémente le contrat de format 1.2.69 sans supprimer de contrôle du parent 0.4.71.

- 390 tests pytest collectés et réussis en suite complète ;
- suite complète également réussie avec ordre de fichiers inversé ;
- baselines historiques `TOP` et `CODES` conservées, contrat actif séparé dans `ACTIVE_TOP` / `ACTIVE_CODES` ;
- les nouveaux paramètres sont exigés pour les paquets 1.2.69 ;
- les quatre anciens noms restent lisibles pour les paquets pré-1.2.69 ;
- les verrous historiques `débat-détaillé` / `detailed-debate` restent vérifiés avec leur ancien nom dans les paquets historiques ;
- coexistence ancien + nouveau nom refusée pour les sorties courantes ;
- 503 exigences, 103 alias et 92 fichiers normatifs vérifiés ;
- aucune disparition par rapport à 1.2.55, 1.2.60, 1.2.61 ou 1.2.68 dans les catégories auditées.
