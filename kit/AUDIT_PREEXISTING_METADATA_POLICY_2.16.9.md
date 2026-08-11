# Audit — politique différentielle des métadonnées préexistantes 1.2.78 / 0.4.81 / 2.16.9

Base : WIKIDEBIA_SOURCES_COMPLETES_1.2.77_0.4.80_2.16.8_2026-08-12.

Décision propriétaire intégrée :

- la règle exigeant un `titre-affiché` propositionnel est une règle de création IA et n’est pas appliquée rétroactivement aux pages déjà présentes sur le wiki ;
- un `titre-affiché` historique est conservé par défaut et n’est modifié que pour orthographe, grammaire, typographie, troncation/corruption, problème flagrant ou décision explicite du propriétaire ;
- le titre canonique / nom de page reste corrigible et doit rester autonome, explicite et non ambigu ;
- les mots-clés historiques d’une page préexistante ne sont pas supprimés pour satisfaire un quota ou une règle de forme de création ; ils peuvent être corrigés (notamment la casse), réordonnés et complétés ;
- la suppression d’un mot-clé historique exige une non-pertinence claire explicitement justifiée ;
- les nouveaux titres affichés et les nouveaux mots-clés produits par Wikidéb’IA restent soumis aux règles de création complètes.

Contrôles exécutés :

- suite kit : 421/421 ;
- suite validateur : 409/409 ;
- test de compatibilité avec le ZIP réel de revue `revenu_de_base_fr_metadata_review_revu_decisions_proprietaire_v2.zip` : les 168 entrées passent la validation individuelle 2.16.9 ;
- cohérence des copies normatives Normes ↔ Validateur : exigée avant scellement ;
- auto-audit du validateur : exigé après scellement des manifestes.
