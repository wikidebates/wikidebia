# Wikidéb’IA — Normes 1.2.50

La révision 1.2.50 sépare strictement deux opérations qui ne doivent plus partager le même profil de rendu : **créer une page** et **modifier une page existante**.

Lors d’une création à partir de zéro, le profil IA reste volontairement restreint et peut ajouter les marqueurs de création prévus. Lors d’une modification, la page existante constitue au contraire un socle à préserver : aucun paramètre top-level autorisé déjà présent ne peut disparaître silencieusement. Les métadonnées historiques (`initialisation` / `initialization`, `nom` / `name`, avertissements, `débat-détaillé` / `detailed-debate`, interlangue existant et date de création) sont conservées exactement par défaut.

Une suppression exige une décision explicite portant sur la page et le paramètre, ou une exception spécialisée déjà attestée. Les marqueurs `Argument généré par IA` / `Débat généré par IA` sont réservés aux créations et ne sont jamais ajoutés rétroactivement à une page existante.

- norme active : `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.50.md` ;
- validateur recommandé : 0.4.53 ;
- kit recommandé : 2.15.27.
