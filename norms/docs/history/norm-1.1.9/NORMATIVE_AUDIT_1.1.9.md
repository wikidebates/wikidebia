# Audit normatif — Wikidéb’IA 1.1.9

## Source active

La source normative active unique est `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.1.9.md`. La norme 1.1.8 est conservée dans `normative_reference/01_normes/history/` comme état historique vérifiable.

La révision 1.1.9 conserve tous les invariants structurels et documentaires antérieurs. Elle ajoute uniquement des exigences éditoriales applicables aux résumés d’arguments :

- la première phrase développe le titre au lieu de le répéter ou de le paraphraser étroitement ;
- les exemples, ordres de grandeur et chiffres restent facultatifs et ne sont utilisés que lorsqu’ils éclairent réellement le raisonnement ;
- toute donnée chiffrée fait l’objet d’une vérification documentaire humaine explicite ;
- un style ferme, imagé et légèrement mordant est admis sans sarcasme, caricature, militantisme ni slogan mécanique ;
- la revue bilingue atteste ces décisions page par page.

## Catalogue et traçabilité

Le catalogue consolidé contient 287 exigences atomiques. Les exigences nouvelles sont `ARG-029` à `ARG-033`. Elles sont reliées à la norme active, au profil de rendu, au workflow et à la matrice de traçabilité.

Les contrôles automatiques ajoutés sont :

- `WDV-EDT-014` — avertissement heuristique lorsque la première phrase est trop proche du titre ;
- `WDV-EDT-015` — erreur lorsqu’une donnée chiffrée détectée ne possède pas l’attestation documentaire humaine exigée.

La pertinence d’un exemple, la qualité d’une image rédactionnelle et le caractère ferme mais non polémique du ton restent des contrôles humains. Aucun score automatique ne peut les remplacer.

## Compatibilité

Le validateur 0.3.1 accepte les paquets déclarés sous les normes 1.1.0 à 1.1.8 sans leur imposer les nouveaux champs 1.1.9. Les nouveaux contrôles bloquants de registre ne s’appliquent qu’aux paquets déclarant `consolidated_norm=1.1.9`.

La commande `validate` demeure strictement en lecture seule. La commande `recalc` reste la seule commande d’écriture locale et exige `--write`. Aucune opération distante n’est autorisée ou implémentée par le validateur.

## Résultat reproductible

- 67 tests réussis ;
- auto-audit UTF-8, fins de ligne, Python et JSON réussi ;
- schéma du catalogue d’exigences validé ;
- compatibilité des registres 1.1.8 testée ;
- aucune constante propre à un corpus introduite ;
- aucun invariant du graphe modifié.

**AUDIT NORMATIF : RÉUSSI**
