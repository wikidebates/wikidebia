# Migration 2.16.14 — deux checkpoints français

Les workflows existants sont repris sans réinitialisation. Si aucune publication française 2.16.13 n’a encore été effectuée, l’orchestrateur publie d’abord le checkpoint graphe/titres puis le checkpoint contenu avant de reprendre un paquet anglais déjà préparé. Si une publication unique 2.16.13 a déjà été attestée, elle est conservée comme état historique non scindable et vaut pour les deux checkpoints lors de la reprise.
