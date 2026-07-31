# Audit de non-régression 0.4.10

Le validateur conserve le comportement 1.2.9 pour les anciens paquets : le modèle générique y reste accepté. Pour les paquets 1.2.10, les tests vérifient qu’une note directe est acceptée, qu’un modèle générique ou spécialisé est refusé, que les références nommées fonctionnent et qu’une date machine dans le texte direct est bloquée.
