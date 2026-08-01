# Changelog

## 0.4.18 — 1er août 2026

- alignement sur la norme 1.2.17 ;
- ajout de `WDV-MWK-019` pour l’article Wikipédia obligatoire ;
- interdiction des paramètres de débats connexes dans les sorties 1.2.17 ;
- ajout de `WDV-DOC-006` contre les tableaux JSON dans `auteurs`/`authors` ;
- compatibilité des révisions antérieures conservée.

## 0.4.18 — 31 juillet 2026

- alignement sur la norme 1.2.17 et le kit 2.2.1 ;
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
