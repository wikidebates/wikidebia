## 0.4.73 — 10 août 2026 — alignement des métadonnées de première publication anglaise

- ne projette plus `initialisation` vers `initialization` dans le chemin `translated_english` d’une nouvelle page ;
- ne compare plus `creation-date` anglaise à `date-création` française ;
- conserve la préservation historique d’`initialization` et de `creation-date` sur les pages anglaises préexistantes ;
- ajoute des régressions d’exécution et restaure l’attribution historique exacte de 0.4.71/0.4.72.

## 0.4.72 — 10 août 2026 — renommage des paramètres MediaWiki

- valide `sujet-développé` / `expanded-topic` et `débat-dédié` / `dedicated-debate` comme paramètres courants ;
- conserve la lecture des anciens noms pour les paquets antérieurs à 1.2.69 ;
- refuse la coexistence des anciennes et nouvelles formes dans une sortie courante.

## 0.4.71 — 10 août 2026 — familles de convergence normalisées

- accepte les reçus de convergence 1.0 et 1.1 ;
- exige pour 1.1 deux `method_family` finales distinctes ;
- conserve tous les contrôles de 0.4.70.

## 0.4.70 — 10 août 2026 — revue idiomatique et corpus réel de régressions

- accepte la revue sémantique 1.4 et le moteur de marqueurs 1.3 ;
- distingue changement idiomatique revu et dégradation formelle ;
- étend les risques lexicaux et le corpus de fixtures réelles ;
- maintient la convergence obligatoire pour les revues 1.3 et 1.4.

## 0.4.69 — 10 août 2026 — équivalence propositionnelle et convergence sémantique

- contrôle le prédicat principal des displayed-title anglais ;
- étend les signaux différentiels et le métadiscours anglais ;
- valide les preuves de champ, les concept_id et le reçu de convergence ;
- ajoute les régressions multiligne et les codes WDV-BIL-008/009, WDV-EDT-033.

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

## 0.4.74 — 10 août 2026 — compatibilité pilotée par schémas et capacités

- ajoute un schéma explicite `wikidebia-validator-report-1.0` aux rapports ;
- centralise les versions courantes dans `VERSIONS.json` ;
- remplace les listes manuelles de révisions compatibles par une dérivation historique informative ;
- conserve les numéros de producteur comme provenance sans les utiliser comme feature flags.

## 0.4.75 — 11 août 2026 — maintenance d’alignement graph-extract

- aucune modification des règles de validation éditoriale ;
- aligne la release sur la norme 1.2.72 et le kit 2.15.56 ;
- conserve `complete_topic` et `detailed_debate` comme clés internes historiques ;
- la régression CLI est corrigée et testée dans le kit.

