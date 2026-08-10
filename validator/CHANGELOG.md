## 0.4.68 — 10 août 2026 — cohérence des documents actifs

- aligne la copie normative sur 1.2.65 ;
- corrige le diagnostic utilisateur qui appelait encore `name=` le champ MediaWiki anglais alors que `name` n’est plus qu’un champ interne de registre ;
- ajoute des tests empêchant le retour des contradictions actives sur l’interlangue différée et les Citation/Quote.

## 0.4.67 — 10 août 2026 — continuité de compatibilité

- restaure `1.2.62` dans `compatible_normative_revisions` et `supported_normative_revisions` ;
- supprime la duplication accidentelle de `1.2.63` ;
- aligne le validateur sur la norme 1.2.64 et le kit 2.15.48, sans changement de logique de validation éditoriale.

## 0.4.66 — 10 août 2026 — correctif de réconciliation

- aligne la copie normative sur 1.2.63 ;
- ajoute des tests garantissant la terminologie active `established-name` / `AI-translated quote` et la cohérence des contrats fusionnés.

## 0.4.65 — 10 août 2026 — réconciliation traduction + publication

- fusionne les deux variantes 0.4.64 développées en parallèle ;
- conserve la validation différentielle FR→EN, les signaux sémantiques structurés, les registres documentaires et les contrôles de scellement ;
- intègre `nom-consacré` / `established-name`, `AI-translated quote`, l'interdiction d'`initialization` sur les nouveaux Arguments EN et les contrôles de cohérence normative de la branche GitHub ;
- combine l'attestation humaine de proposition/intelligibilité avec le contrôle différentiel sans permettre à une attestation générique d'annuler une régression FR→EN ;
- aligne les schémas et la copie normative sur 1.2.62.

Les changelogs complets des deux branches 0.4.64 sont conservés sous `branch_history/`.
