# Migration vers la norme 1.2.16

1. Installer la norme 1.2.16, le validateur 0.4.17 et le kit 2.2.0.
2. Conserver les versions historiques inscrites dans les corpus déjà produits.
3. Pour une reprise, fournir ou laisser retrouver un état publié antérieur signé ; aucune suppression n’est permise sans cette preuve.
4. Déclarer les renommages et fusions dans `data/remote_migrations.json` lorsqu’ils ne peuvent pas être déduits de l’identité logique.
5. Exécuter `./wikidebia update IDENTIFIANT --dry-run`, examiner les opérations `manual_review` et `blocked`, puis confirmer l’empreinte du plan pour une exécution réelle.
6. Utiliser `--no-delete` pour une reprise conservatrice ou `--only-delete` après publication préalable et vérifiée des nouvelles pages.

La commande historique de mise à niveau des composants devient `./wikidebia upgrade`.
