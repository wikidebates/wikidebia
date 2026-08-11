# Audit de régression kit 2.15.56

- 375 tests réussis ;
- reproduction du crash `AttributeError: Namespace ... follow_local_relations_at_detailed_debate` ajoutée à la suite ;
- nouveau nom `dedicated-debate` testé via le trajet réel `argparse → main()` ;
- alias historique `detailed-debate` testé et conservé ;
- aucune occurrence `args.follow_local_relations_at_detailed_debate` ne subsiste dans le code actif ;
- les occurrences de `complete_topic` et `detailed_debate` restantes sont des clés techniques internes ou des tests de compatibilité explicitement conservés ;
- aucune régression des 372 tests du parent.
