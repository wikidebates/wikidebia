# Wikidéb’IA — Normes 1.2.57

La révision 1.2.57 fixe les conventions des futures traductions FR→EN : résumé anglais `Translation of the French page: [[:fr:X|X]]`, résumé français d’ajout interlangue `Ajout du lien interlangue vers la page anglaise : [[:en:X|X]]`, avertissement `AI-translated quote` et double balise de création `chatgpt` + `translated-fr`. Elle conserve sans les relâcher les règles éditoriales cumulatives antérieures, notamment la traduction adaptative, la recherche de `name=` consacrés, la préservation des paramètres historiques et des résumés historiquement absents.

Lors d’une création à partir de zéro, le profil IA reste volontairement restreint et peut ajouter les marqueurs de création prévus. Lors d’une modification, la page existante constitue au contraire un socle à préserver : aucun paramètre top-level autorisé déjà présent ne peut disparaître silencieusement. Les métadonnées historiques (`initialisation` / `initialization`, `nom` / `name`, avertissements, `débat-détaillé` / `detailed-debate`, interlangue existant et date de création) sont conservées exactement par défaut.

Une suppression exige une décision explicite portant sur la page et le paramètre, ou une exception spécialisée déjà attestée. Les marqueurs `Argument généré par IA` / `Débat généré par IA` sont réservés aux créations et ne sont jamais ajoutés rétroactivement à une page existante.

### Correctif de traduction FR→EN du 7 août 2026

Pendant la traduction, la page anglaise cible est ignorée comme source éditoriale. Les métadonnées françaises de progression et d'avertissement sont traduites par la table exhaustive de `docs/GUIDE_TRADUCTION_METADONNEES_FR_EN.md` ; aucune valeur de création par défaut n'est ajoutée à une traduction et un champ absent reste absent. Les débats connexes ne sont projetés que si leur page anglaise correspondante existe. Chaque lot reçoit une seconde passe de comparaison FR→EN avant clôture.

- norme active : `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.57.md` ;
- validateur recommandé : 0.4.61 ;
- kit recommandé : 2.15.42.
