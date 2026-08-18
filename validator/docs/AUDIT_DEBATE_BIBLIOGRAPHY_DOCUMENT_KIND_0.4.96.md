# Audit WDV-SRC-005 — Validator 0.4.96

`WDV-SRC-005` vérifie la fonction documentaire d’une référence bibliographique de page Debate : l’usage doit être `foundational_work` ou `broad_synthesis` et disposer d’une justification substantielle.

Le filtre historique limitant `document_kind` à six catégories de synthèse a été retiré, car la norme privilégie ces formes sans en faire une enum exhaustive. Un texte juridique officiel peut être retenu s’il remplit réellement la fonction large déclarée. Une source `narrow_argument` ou insuffisamment justifiée reste rejetée.
