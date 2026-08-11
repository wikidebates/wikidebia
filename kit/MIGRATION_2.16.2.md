# Migration 2.16.2

Aucun reset n’est requis. Un workflow créé par 2.16.1 avec `short_code` absent peut être relancé tel quel : le code est dérivé automatiquement du `debate_id`. Un `--short-code` explicite peut également réparer cet état tant qu’il ne contredit pas un code valide déjà enregistré.
