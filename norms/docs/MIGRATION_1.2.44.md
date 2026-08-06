# Migration vers la norme 1.2.44

La révision 1.2.44 distingue les simples notices documentaires des phrases explicatives dans les balises `<ref>`. Une notice ne se termine jamais par un point avant `</ref>` ; la ponctuation de la phrase principale suit l'appel de note.

Un point terminal interne reste possible pour une phrase explicative complète, à condition que son corps exact soit attesté par SHA-256 dans `terminal_period_sentence_exceptions`. Les corpus historiques peuvent activer uniquement cette règle avec `editorial_controls.inline_reference_punctuation_policy_revision=1.2.44`.
