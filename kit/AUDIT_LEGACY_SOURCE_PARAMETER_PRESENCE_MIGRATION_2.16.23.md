# Audit kit 2.16.23 — migration de présence top-level

## Défaut corrigé

Une revue `fr_content_review` déjà `approved` et un `content-reviewed-copy` déjà `fr_content_applied` sous une version antérieure à 2.16.22 pouvaient être réutilisés idempotemment sans recevoir `source_parameter_presence`. Le renderer 2.16.22 savait préserver `|paramètre=`, mais l’ancien verrou ne contenait pas la preuve nécessaire.

## Correction

- `_build_content_copy()` redérive la présence depuis `reviewed-copy` via `_source_imports()` et ne dépend pas du champ éditable du ZIP ;
- `apply_review()` détecte un verrou ancien incomplet ;
- la reconstruction est autorisée uniquement si aucun état de checkpoint `content` n’existe ;
- tout état de checkpoint existant bloque la migration destructive et doit être repris par le workflow transactionnel ;
- le SHA de la revue éditoriale n’est pas réécrit.

## Régression réelle

Le scénario vote électronique est couvert : une revue approuvée/appliquée avant 2.16.22 est reprise, puis `A0021|objections=`, `bibliographie-pour=` et `vidéographie-contre=` retrouvent leur preuve de présence avant rendu.
