# Migration du kit 2.2.3

Le kit 2.2.3 rétablit la mise à niveau à partir d’un seul ZIP complet. Le bundle doit être le seul fichier ZIP de `updates/` et contenir les trois composants stables `wikidebia-normes.zip`, `wikidebia-validator.zip` et `wikidebia-kit.zip`.

Depuis un lanceur antérieur où `update` désigne encore la mise à niveau des composants :

```bash
rm -f updates/*.zip
cp WIKIDEBIA_*.zip updates/
./wikidebia update --no-git
```

Après installation du kit 2.2.3, les mises à niveau suivantes utilisent :

```bash
./wikidebia upgrade
```

Les ZIP de composants livrés dans le bundle n’embarquent pas leur reçu auto-référentiel, afin de rester acceptés par le gestionnaire historique 2.1.17. Les reçus restent fournis au niveau de la livraison complète. Le gestionnaire 2.2.3 accepte néanmoins un `PACKAGE_RECEIPT.json` facultatif et le vérifie lorsqu’il est présent.
