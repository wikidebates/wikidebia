# Wikidéb’IA — Normes 1.2.55

La révision 1.2.55 affine la traduction anglaise après retour des premiers lots : unités internes de 10 arguments par défaut (5–8 lorsqu'elles sont denses), agrégation possible pour les gros travaux, recherche de `name=` sensible à la forme anglaise réellement consacrée et à la portée exacte du raisonnement, et principe explicite d'exécution non mécanique. Elle corrige aussi le workflow afin qu'un résumé historiquement absent en français reste absent en anglais.

Lors d’une création à partir de zéro, le profil IA reste volontairement restreint et peut ajouter les marqueurs de création prévus. Lors d’une modification, la page existante constitue au contraire un socle à préserver : aucun paramètre top-level autorisé déjà présent ne peut disparaître silencieusement. Les métadonnées historiques (`initialisation` / `initialization`, `nom` / `name`, avertissements, `débat-détaillé` / `detailed-debate`, interlangue existant et date de création) sont conservées exactement par défaut.

Une suppression exige une décision explicite portant sur la page et le paramètre, ou une exception spécialisée déjà attestée. Les marqueurs `Argument généré par IA` / `Débat généré par IA` sont réservés aux créations et ne sont jamais ajoutés rétroactivement à une page existante.

### Correctif de traduction FR→EN du 7 août 2026

Pendant la traduction, la page anglaise cible est ignorée comme source éditoriale. Les métadonnées françaises de progression et d'avertissement sont traduites par la table exhaustive de `docs/GUIDE_TRADUCTION_METADONNEES_FR_EN.md` ; aucune valeur de création par défaut n'est ajoutée à une traduction et un champ absent reste absent. Les débats connexes ne sont projetés que si leur page anglaise correspondante existe. Chaque lot reçoit une seconde passe de comparaison FR→EN avant clôture.

- norme active : `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.55.md` ;
- validateur recommandé : 0.4.58 ;
- kit recommandé : 2.15.32.
