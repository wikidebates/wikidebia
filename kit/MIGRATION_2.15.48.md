# Migration 2.15.48

Correctif de preuve de tests : deux modules historiques chargeaient des scripts par `importlib` sans rendre le dossier `scripts/` importable. La suite complète masquait ce défaut grâce aux effets de bord de modules collectés auparavant. Les deux tests sont désormais auto-suffisants et vérifiés par sous-processus isolé.
