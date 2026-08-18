# Audit — normalisation des vérifications documentaires anglaises — kit 2.16.25

Le défaut reproduit provient d'un paquet `en_translation_review` où les nouvelles sources anglaises utilisaient encore `verification.checked_at`, `verification.method` et `verification.note`. La finalisation de la revue acceptait ce format, puis `_build_translated_copy()` le recopiait sans normalisation dans le registre canonique `data/sources.json`, dont le schéma exige `verified_at`, `primary_source` et `notes`.

Le correctif applique une normalisation uniquement à la frontière de projection finale. `checked_at` devient `verified_at`; `note` et `method` alimentent `notes`; les anciennes clés sont supprimées. Lorsqu'une revue historique n'a jamais enregistré `primary_source`, la valeur devient `null` et le validateur 0.4.94 l'accepte comme état de compatibilité explicite. Aucun booléen documentaire n'est inventé.

Les nouvelles revues utilisent le format canonique et doivent fournir un `primary_source` booléen. La preuve de convergence sémantique demeure valable, car cette migration ne modifie ni titres, ni résumés, ni introduction, ni aucun autre champ inclus dans `semantic_content_sha256`.
