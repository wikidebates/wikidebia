# Changelog

## 0.4.24 — 1er août 2026

- alignement sur la norme 1.2.22 ;
- réactivation bloquante de `WDV-EDT-001` lorsque plus de 10 % des titres affichés copient exactement les titres canoniques dans une langue ;
- attestations de concision obligatoires dans le registre individuel ;
- justification spécifique obligatoire pour chaque identité exacte conservée ;
- maintien de `WDV-EDT-021`, `WDV-EDT-022` et de la compatibilité 1.1.0–1.2.21.

## 0.4.23 — 1er août 2026

- alignement sur la norme 1.2.21 ;
- conservation de `WDV-EDT-022` pour les corpus 1.2.20 et 1.2.21 ;
- correction des identifiants de traçabilité du placement (`GR-048` à `GR-050`) ;
- tests renforcés sur les structures réelles des arêtes et sur la non-rétroactivité ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.20.


## 0.4.22 — 1er août 2026

- alignement sur la norme 1.2.20 ;
- ajout du contrôle bloquant `WDV-EDT-022` ;
- contrôle d’un registre couvrant toutes les occurrences actives ;
- tests renforcés pour empêcher la promotion au niveau 1 d’objections ciblées et d’exemples spécialisés ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.19.

## 0.4.21 — 1er août 2026

- alignement sur la norme 1.2.19 ;
- ajout de `WDV-EDT-021` pour les titres affichés manifestement réduits à un groupe nominal ;
- ajout des attestations bilingues obligatoires de complétude propositionnelle et d’intelligibilité dans la revue individuelle ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.18 sans activation rétroactive ;
- aucune écriture distante.


## 0.4.20 — 1er août 2026

- maintien de tous les contrôles 0.4.19 ;
- correction de l’exemple anglais de la norme active, qui ne montre plus `wikipedia-articles` vide ;
- ajout d’un test de non-régression sur les squelettes Débat/Debate actifs ;
- copie normative resynchronisée octet par octet.

## 0.4.19 — 1er août 2026

- alignement sur la norme 1.2.18 ;
- ajout de `WDV-DOC-007` pour la virgule canonique entre auteurs ;
- refus du point-virgule, des virgules mal espacées et de la virgule pleine chasse sous 1.2.18 ;
- compatibilité historique conservée jusqu’à 1.2.17.


## 0.4.18 — 1er août 2026

- alignement sur la norme 1.2.17 ;
- ajout de `WDV-MWK-019` pour l’article Wikipédia obligatoire ;
- interdiction des paramètres de débats connexes dans les sorties 1.2.17 ;
- ajout de `WDV-DOC-006` contre les tableaux JSON dans `auteurs`/`authors` ;
- compatibilité des révisions antérieures conservée.

## 0.4.17 — 31 juillet 2026

- alignement sur la norme 1.2.16 et le kit 2.2.0 ;
- ajout des schémas d’état publié, de migrations, de plan et de reçu de reprise ;
- ajout de `validate-plan`, strictement local et en lecture seule ;
- contrôles WDV-RMT-001 à WDV-RMT-006 sur l’intégrité et la sécurité des plans distants ;
- aucune connexion ni écriture MediaWiki dans le validateur.

## 0.4.16 — 31 juillet 2026

- chemins de paquet absolus rendus indépendants du dossier courant ;
- aucun fragment de chemin absolu local n’est conservé dans les rapports ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.15 ;
- alignement des métadonnées avec le kit 2.1.17.

## 0.4.15 — 31 juillet 2026

- alignement sur la norme 1.2.15 ;
- conservation de tous les contrôles du validateur 0.4.13 ;
- prise en charge des paquets déclarant 1.2.15 ;
- copie normative synchronisée avec la correction séparant le nom du ZIP du `debate_id` interne.

## 0.4.13 — 30 juillet 2026

- alignement sur la norme 1.2.13 ;
- copie normative mise à jour pour le dossier unique `incoming/` et la sélection des ZIP par identifiant ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.12 ;
- aucun changement des contrôles de contenu par rapport à 0.4.12.

## 0.4.12 — 30 juillet 2026

- alignement sur la norme 1.2.12 et le kit 2.1.12 ;
- rapports portables : `package_root` ne conserve plus de chemin absolu ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.11 ;
- copie normative et exemples actifs mis à jour.


## 0.4.11 — 30 juillet 2026

- alignement sur la norme 1.2.11 ;
- ajout du contrôle bloquant `WDV-MWK-018` ;
- détection des séquences `}}` suivies d’un ou plusieurs retours à la ligne puis de `{{`, avec espaces ou tabulations facultatifs ;
- forme canonique exigée : `}}{{` ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.10.

## 0.4.10 — 30 juillet 2026

- alignement sur la norme 1.2.10 ;
- remplacement du modèle générique `Référence`/`Reference` par des notes d’introduction rédigées directement ;
- refus de tout modèle MediaWiki dans le corps d’une note développée d’introduction ;
- contrôle des dates machine dans le texte direct des notes ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.10.

## 0.4.9 — 30 juillet 2026

- alignement sur la norme 1.2.9 ;
- refus des dates documentaires au format ISO machine, sans toucher aux dates de création ;
- contrôle du modèle générique `Référence`/`Reference` dans les introductions ;
- minimum de deux notices dans chacun des neuf paramètres documentaires de Débat/Debate ;
- contrôle de l’usage des acronymes courants déclarés dans `sujet-complet`/`complete-topic` ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.9.

## 0.4.8 — 29 juillet 2026

- alignement sur la norme 1.2.8 ;
- contrôle bloquant de l’ordre alphabétique des rubriques et sections par langue ;
- contrôle bloquant de la majuscule initiale de `sujet` et `topic` ;
- détection heuristique bloquante des formes interrogatives dans `sujet-complet` et `complete-topic` ;
- extension des registres de revue à la précision des rubriques, à la profondeur documentaire et à la force expressive ;
- ajout de 1.2.7 et 1.2.8 à la condition de schéma exigeant les contrôles éditoriaux ;
- auto-audit des étiquettes de provenance, des chemins normatifs et de la révision des exemples actifs ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.8.

## 0.4.5 — 28 juillet 2026

- alignement sur la norme 1.2.5 ;
- suppression du minimum automatique d’un appel `<ref>` par introduction ;
- maintien de l’interdiction des balises `<references />` et du contrôle de la revue humaine.
