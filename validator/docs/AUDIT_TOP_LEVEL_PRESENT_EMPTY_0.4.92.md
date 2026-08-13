# Audit validateur 0.4.92 — paramètres top-level présents et vides

## Défaut corrigé

`WDV-MWK-005` interdisait toute valeur top-level vide alors que la norme 1.2.86 et le kit 2.16.22+ exigent parfois de conserver la présence historique d’un paramètre devenu vide.

## Garde-fou

L’exception n’est accordée que si :

1. la page est française ;
2. son manifeste déclare `page_origin=preexisting` ;
3. `data/fr_content_lock.json` contient la page exacte ;
4. `source_parameter_presence[paramètre].present=true`.

Sans cette preuve, `WDV-MWK-005` reste bloquant. Les sous-paramètres documentaires vides conservent leurs contrôles propres.
