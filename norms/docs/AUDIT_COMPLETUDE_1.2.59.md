# Audit de complétude — norme 1.2.59

## Objet

Vérifier que la nouvelle règle de métadonnées de création des traductions anglaises est circonscrite et ne régresse pas la migration 1.2.58 de `nom-consacré` / `established-name`.

## Contrôles requis

- le paramètre MediaWiki d’appellation consacrée reste `nom-consacré` en français et `established-name` en anglais ;
- les alias historiques `nom` / `name` restent réservés à la préservation d’anciennes pages et les champs JSON génériques `name` restent inchangés ;
- une nouvelle traduction anglaise d’Argument ne peut pas publier `initialization` ;
- aucune valeur de `initialisation` française n’est projetée vers le wiki anglais ;
- chaque nouvelle page anglaise traduite reçoit `creation-date` égale au jour réel de sa création distante ;
- cette date n’est ni `date-création` française ni la date de traduction/rendu ;
- la date est contrôlée page par page avant écriture afin de traiter correctement un passage de minuit ;
- une reprise après création partielle conserve la date des pages déjà créées et redéfinit la date uniquement pour les pages restant à créer ;
- les pages anglaises préexistantes restent sous politique de préservation historique ;
- les règles 1.2.57 de résumé, `AI-translated quote` et double balise `chatgpt` + `translated-fr` restent inchangées.
