# Migration 1.2.53

Cette révision formalise le protocole de traduction anglaise après validation du corpus français. La page Debate est traitée dans un lot autonome ; les pages Argument sont traduites par lots de 20 pages par défaut (25 maximum, 10–15 lorsque la documentation ou les citations sont denses), puis une passe globale inter-lots précède la finalisation.

`name=` anglais fait toujours l'objet d'une recherche propre à la littérature anglophone. Les références françaises ne sont jamais traduites comme notices : seule une version anglaise réellement publiée et vérifiée peut être projetée, avec ses propres métadonnées, et de nouvelles références anglophones sont recherchées indépendamment.

Le contrat spécial `Citation`→`Quote` reste inchangé : seules les valeurs de `quote` et `date` sont traduites, les autres valeurs sont préservées et `Citation traduite par IA` est ajouté à `warnings`.
