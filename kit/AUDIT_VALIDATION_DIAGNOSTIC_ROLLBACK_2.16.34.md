# Audit — persistance des diagnostics pendant le rollback (2.16.34)

Le diagnostic de validation introduit en 2.16.33 était créé dans `outgoing/` avant que `review-import` ne restaure sa transaction locale. Le rollback supprimait ensuite tout enfant nouveau de `outgoing/`, y compris le diagnostic, ce qui expliquait un dossier vide malgré la génération correcte du ZIP.

Le correctif 2.16.34 rend les diagnostics auto-identifiés persistants à travers ce rollback. L’exemption exige simultanément un nom `*_diagnostic.zip`, un membre `DIAGNOSTIC_PACKAGE.json`, le schéma `wikidebia-workflow-diagnostic-package-1.0`, la version de schéma `1.0` et un `error_count` strictement positif. Les autres sorties nouvelles restent soumises au nettoyage transactionnel.

Régressions : un diagnostic de sept erreurs survit ; un paquet partiel est supprimé ; un faux diagnostic est supprimé.
