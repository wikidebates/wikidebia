# Changelog

## 0.3.0 — 26 juillet 2026

- alignement sur la norme consolidée 1.1.8 ;
- style encyclopédique grand public obligatoire pour les résumés d'arguments ;
- définition intégrée des termes techniques nécessaires lors de leur première occurrence utile ;
- nouveau contrôle `WDV-EDT-013` : avertissement heuristique sur l'accumulation de phrases longues et contrôle de la revue humaine page par page ;
- seuils de lisibilité déclarés par le paquet, sans constante propre à un débat ;
- conservation de tous les contrôles 0.2.9.


## 0.2.4 — 25 juillet 2026

- prise en charge de la norme 1.1.2 ;
- contrôle des guillemets droits ASCII dans les titres canoniques et affichés ;
- deux à quatre mots-clés thématiques par argument ;
- contrôle de longueur, taille du vocabulaire et réutilisation sur plusieurs pages ;
- vocabulaire W10.R3 et rapports de traçabilité dédiés.

## 0.2.3 — 2026-07-25

- alignement sur la norme consolidée Wikidéb’IA 1.1.1 ;
- détection bloquante des ellipses, articles mutilés et connecteurs pendants dans les titres affichés ;
- vocabulaire bilingue contrôlé de mots-clés, avec trois à cinq groupes nominaux par page ;
- contrôle de traduction des keywords et de l’asymétrie forte des résumés bilingues ;
- prise en charge des reprises correctives 1.1.0 et 1.1.1 sans invalider les handoffs historiques ;
- trente et un tests réussis, zéro échec.

## 0.2.0 — 2026-07-23

- alignement sur le paquet normatif Wikidéb’IA 1.1.0 et ses quinze JSON Schema ;
- intégration du catalogue de 252 exigences et de la matrice de traçabilité ;
- prise en charge d’une vidéographie sans auteur uniquement lorsque le registre documentaire justifie cette absence ;
- contrôle numérique de `numéro=` et `issue=` ;
- contrôle de la langue des dates et de certains lieux documentaires ;
- contrôle du placement français des appels `<ref>` avant la ponctuation finale ;
- validation des manifestes individuels de pages et de lots ;
- validation des copies de staging interlangue dans les paquets de migration ;
- premier test pilote réel sur 171 arguments bilingues, 344 pages et 28 lots ;
- seize tests unitaires et d’intégration réussis.

## 0.1.0 — 2026-07-23

- première version complète du validateur stable ;
- validation Schema, graphe, lots, sources, fichiers, wikicode, bilingue et workflow ;
- rapports texte et JSON à codes stables ;
- mode de recalcul séparé ;
- treize tests positifs et négatifs.

## 0.2.3 — 2026-07-25

- contrôle bloquant des ellipses, articles tronqués, débuts minuscules, connecteurs pendants et répétitions dans les titres affichés ;
- vocabulaire bilingue contrôlé obligatoire pour les mots-clés de la norme 1.1.1 ;
- contrôle du nombre, de la nature nominale, de la traduction et de la diversité des mots-clés ;
- contrôle heuristique de l'équivalence de longueur des résumés bilingues ;
- prise en charge de la reprise W10.R2.


## Version 0.2.9
La version 0.2.9 remplace les quotas globaux de titres et rubriques par une revue éditoriale individuelle obligatoire de tous les nœuds actifs (`WDV-EDT-012`). Aucune rubrique n’est traitée spécialement : chacune doit être justifiée pour chaque page où elle est retenue.

## 0.2.9

- justification générique de chaque rubrique ;
- date, rapports et handoff déclarés par le paquet ;
- contrôle statique contre les constantes propres à un corpus.

## 0.2.9
Valeurs d’avertissement par/by, norme 1.1.7 et contrôles de publication traçable.
