# Relecture française–anglaise du débat cannabis — 21 octobre 2026

**État : textes relus et corrigés ; documentation et intégration native incomplètes. Aucune publication.**

La version 2 d’origine est conservée intacte. Son SHA-256 est `b317df79f35b047af2bdead55c5adbdb33c835fae528ed69f0de78e5d8332eda`. La copie `working/` ci-jointe poursuit cette livraison ; elle ne remplace pas rétroactivement son archive ni les sources françaises.

## Travail réellement effectué

La traduction initiale provient d’une autre conversation. La première reprise avait essentiellement contrôlé l’intégrité et commencé la recherche documentaire ; elle ne constituait pas une lecture personnelle détaillée des 153 pages.

Cette relecture a comparé les textes français et anglais des 153 fiches : titres, résumés lorsqu’ils existent, citations intégrales, deux passages entre citations et libellés des justifications/objections. Les quatre fichiers `notes-001.json` à `notes-004.json` contiennent une note propre à chaque fiche. Une passe complémentaire a repris tous les titres, les libellés distincts et les 32 résumés, avec attention aux négations, modalités, intensités, conditions et portées. Il ne s’agit pas d’une revendication de conformité au protocole de lots documentaires clos ni d’un reçu de convergence officiel.

Les consignes relues incluent `kit/GUIDE_TRANSLATION_REVIEW.md`, `kit/GUIDE_BILINGUAL_RENDER.md` et `norms/docs/GUIDE_TRADUCTION_METADONNEES_FR_EN.md`. Les règles de génération de nouveaux débats ne sont pas appliquées aux textes historiques.

## Corrections

18 interventions ciblées sont consignées avant/après dans `corrections.json` : trois titres (production/culture, très lucrative, personnes précaires), suppression du titre de sous-partie ajouté sans équivalent source, des coordinations de résumés/citations et autres écarts de portée, traduction d’assuétude, conservation de la notion de létalité, localisation vérifiée du lien Weather Underground, puis six listes de mots-clés. Le journal fait foi pour le détail exact des 18 interventions ; plusieurs concernent des passages identiques.

`Interdiction` devient `ban`, distinct de `Prohibition` → `prohibition`, ce qui retire cinq doublons introduits par la traduction. `Contrôle` devient `control`. Deux autres répétitions de mots-clés existaient déjà dans le français (A0042 et A0043) : elles sont signalées et conservées, sans nettoyage silencieux. Les rubriques et mots-clés constituent deux espaces de noms ; la rubrique Droit et le mot-clé Loi ne créent pas de collision entre mots-clés réels. La table contient 59 mots-clés utilisés ; ce n’est pas encore le registre natif approuvé, dont les entrées françaises restent vides.

Aucun résumé absent n’est ajouté, aucune citation n’est supprimée. Aucune source française n’est réécrite. Les dates de création et initialisations françaises restent absentes en anglais.

## Résultats techniques

`final-integrity-audit.json` contient 1 794 assertions réussies, dont beaucoup sont des contrôles répétitifs par page ou citation ; ce nombre ne mesure pas la qualité éditoriale. Couverture : 153 pages, 149 citations dont 145 dates, 32 résumés, 120 absences de résumé, 170 relations (13 racines et 157 entre arguments), 165 libellés distincts.

`parameters-after.json` classe chaque paramètre source et compare les métadonnées des 149 citations : attributions, œuvres, articles, éditeurs, liens et dates sont conservés conformément au contrat. Les textes anglais des citations et leurs dates traduites, ainsi que l’avertissement obligatoire, sont les seules valeurs adaptées. Aucun nom de paramètre anglais inattendu ni doublon de nom n’est trouvé. Les deux passages entre citations restent présents et ancrés avant Q035 et Q121. Les champs documentaires sont explicitement marqués ouverts, pas déclarés conformes par omission.

Les 145 dates du corpus sont équivalentes. Le validateur ne comparait auparavant pas certains formats numériques français : le correctif les reconnaît, conserve leur précision et bloque désormais les formats inconnus ou impossibles. Le correctif de code reste dans la PR en brouillon nº 9, sans fusion. La conservation des passages entre citations est également couverte par cette PR.

Validation du code : 667 tests kit réussis, suite validateur réussie, 22 tests de déploiement réussis et auto-audit réussi. Les vérifications GitHub sont enregistrées séparément lorsqu’elles sont disponibles.

## Ce qui empêche de déclarer « tout bon »

- La recherche anglophone indépendante page par page et les recherches de noms consacrés restent incomplètes. Les requêtes automatisées de découverte ne valent pas vérification documentaire.
- Certaines références françaises restent dans l’introduction ou des résumés : aucune édition anglaise n’est inventée, aucune citation n’est retirée pour cette raison.
- Le logo français `Logo_debat_cannabis.jpg` n’a pas été projeté par la version 2 : il est absent de Commons et son existence locale sur le wiki anglais reste non vérifiée (403). La carte de A0058 existe, mais son actualité et ses contestations restent à revoir.
- Certaines citations présentent des incohérences ou des problèmes documentaires déjà signalés (notamment Q063/Q064/Q069/Q103, Q117 et Q120). La fidélité au texte français ne certifie pas leur authenticité ou leur exactitude factuelle.
- Le corpus natif est encore `graph_draft`, sans tous les verrous et revues français requis ; les lots officiels anglais, la finalisation et les deux passes de convergence sur une revue scellée ne sont pas accomplis. Les fichiers de cette livraison ne doivent pas être présentés comme ces verrous.

Aucune page wiki n’a été publiée ; aucun environnement n’a été republié ; aucune branche de publication française n’a été fusionnée.
