# Reprise du 21 octobre 2026 : documentation sélectionnée et raccord natif

La traduction relue de 153 pages est conservée. Cette reprise ajoute une sélection documentaire indépendante et raccorde les données aux structures réelles du kit. **Ce dossier n'est pas une validation documentaire complète, une convergence sémantique officielle ou une autorisation de publication. Aucune page wiki n'a été publiée.**

## Copie à utiliser

La seule copie retenue à l'issue de cette reprise est `corpus/` dans le paquet, issue de `working-selected/` dans l'environnement. Les dossiers locaux `working/`, `working-interrupted-0/` et `working-selected-interrupted-1/` restent conservés comme historique et ne sont pas des livraisons. Le premier brouillon documentaire ajoutait des sources contextuelles : il a été écarté, puis la sélection a été reconstruite depuis la copie intégralement relue.

La provenance demeure la VERSION 2 VÉRIFIÉE, SHA-256 `b317df79f35b047af2bdead55c5adbdb33c835fae528ed69f0de78e5d8332eda`. Les identifiants A0001…A0152 de cette livraison ne sont pas les identifiants natifs. Les raccords contrôlent le titre français, sa révision et le SHA-256 du wikicode ; seules les apostrophes normalisées diffèrent dans trois titres natifs.

## Travail conservé et effectué

- La comparaison bilingue individuelle des 153 pages et ses 153 notes sont conservées dans `reviews/textual/`. Dix-huit corrections ciblées de la relecture précédente restent appliquées sur 17 pages. Cette reprise documentaire ne change aucun titre, résumé, texte de citation, passage entre citations, mot-clé, rubrique ou lien argumentatif de cette copie relue.
- 40 références anglaises réelles sont retenues sur 106 pages, dont le Débat. Chaque sélection et chaque rejet de référence du brouillon ont une justification par page. Aucune référence n'est ajoutée uniquement pour remplir une rubrique ; les 47 autres pages n'ont pas reçu d'ajout insuffisamment pertinent.
- Les références comprennent notamment les analyses des marchés et régimes de RAND, le bilan canadien, l'analyse Brookings du dispositif uruguayen et de ses difficultés internationales, les conventions primaires de 1961 amendée et de 1988, et des travaux scientifiques anglais sur les usages, les risques, les prix, les collisions et les substitutions. L'identité du document et la portée réellement consultée sont indiquées. Un résumé scientifique consulté n'est jamais présenté comme la lecture intégrale de l'article.
- Les études contradictoires ne sont pas utilisées comme seules références d'une page qu'elles réfutent. Lorsqu'un document développe le mécanisme de l'argument avant d'en discuter les limites, cette contribution et les objections sont indiquées. Exemple : l'association opioïdes/cannabis de 2014 et sa non-réplication en 2019 sont distinguées.
- La sélection ne valide pas toutes les assertions historiques des citations : elle étaye des mécanismes identifiés, avec leurs limites de pays, période, population et causalité. Les citations françaises et leurs attributions n'ont pas été corrigées silencieusement.

## Contrôles effectivement réussis

- **1 794 assertions d'intégrité** : 153 pages, 149 citations, 145 dates de citation, 32 résumés, 120 absences de résumé, 170 occurrences de relations, 165 libellés distincts ; données/rendu cohérents ; snapshot français d'origine inchangé.
- **921 contrôles complémentaires** : invariance de tous les champs non documentaires par rapport à la relecture complète, références rendues exactement conformes à la sélection enregistrée, usages documentaires, identité révision/hash dans la provenance native, absence de faux verrou final.
- Comparaison exhaustive des paramètres des modèles : zéro paramètre dupliqué et zéro anomalie structurelle non résolue. Les deux répétitions de mots-clés déjà présentes en français restent préservées ; les dates de création et initialisations françaises ne sont pas copiées vers l'anglais.
- **Validateurs natifs du kit** : registre des 40 sources sélectionnées accepté ; les 149 traductions de citations et les deux passages hors `Citation` passent les fonctions natives de validation. Les autres paramètres des citations sont conservés ; seules la traduction, la date linguistique équivalente et l'avertissement requis changent. Deux rapports lexicaux courts ont été revus explicitement : Q092 et Q120 donnent déjà le texte anglais suivi de son doublon français dans la source ; l'anglais complet est conservé.

Ces résultats portent sur leur périmètre déclaré. Ils ne signifient pas que toutes les exigences éditoriales du kit sont closes.

## État réel du kit

Le corpus français a été importé dans un projet natif distinct, le graphe a été relu, finalisé et promu, puis les 153 titres français ont été verrouillés **sans aucune opération de réécriture française**. Le workspace est au statut `fr_content_review_ready`.

Le fichier `native/project/.state/editorial-workspaces/cannabis/EN-CANNABIS-20261021/reviews/en/translation_review.pending.json` reprend les vrais constructeurs du kit et les identités natives. Il contient les textes et les sous-revues de citations validées. C'est **une fiche préparatoire en attente**, pas le résultat de la commande officielle `--prepare` : le verrou français du contenu est encore absent. Les 20 unités de revue calculées restent ouvertes ; aucun ancien travail n'est requalifié rétrospectivement en lots officiellement clos.

Le code utilisé est la branche `fix/preserve-interquotation-prose`, commit `4b2abbe`, PR brouillon https://github.com/wikidebates/wikidebia/pull/9. Les tests du code avaient passé (667 tests du kit, contrôles du validateur et du déploiement, auto-audit et CI). Aucun code n'a été modifié pendant cette reprise documentaire ; les contrôles de données ci-dessus ont été exécutés sur la copie retenue.

## Points qui empêchent encore une validation complète

1. **Préservation française et chemin natif.** La finalisation française exige une sélection structurée des notices et des décisions de classification ; les références historiques brutes ne doivent pas disparaître pour ouvrir artificiellement l'étape anglaise. Certaines absences de rubriques/mots-clés ont reçu des valeurs d'import par défaut dans le projet natif ; elles ne sont pas projetées en anglais comme si elles existaient en français. Les cas exacts sont inventoriés. Aucun verrou français du contenu ni verrou anglais final n'a été fabriqué.
2. **Assertions documentaires non confirmées.** Les 260 000 emplois d'A0014 ne sont pas présents dans la page Hyperdébat effectivement consultée. Le lien Croix-Bleue d'A0143 traite d'un classement de dommages mais n'établit pas la classification « alcool = drogue dure » ; il contient aussi une incohérence de score par rapport à Nutt. Les textes historiques traduits sont préservés, mais les attestations de vérification quantitative ne sont pas cochées à tort.
3. **Authenticité des citations.** Q063, Q064, Q069 et Q103 n'ont notamment pas d'attribution exacte authentifiée. Leurs intitulés bibliographiques ressemblent à des notices qui n'ont pas été retrouvées de façon concluante. Cela n'autorise ni leur suppression, ni l'invention d'une édition anglaise, ni une déclaration d'authenticité. Pour les autres citations aussi, fidélité de traduction et authenticité externe restent deux vérifications différentes.
4. **Recherche d'appellations.** Les recherches terminologiques et les sources réellement consultées sont conservées. Les résultats Bing des requêtes par page sont très souvent hors sujet ; ils sont explicitement rejetés comme preuve d'absence de nom consacré. Les notions générales (harm principle, reactance, etc.) ne sont pas transformées en noms d'arguments. Aucun nouveau `established-name=` n'est ajouté ; la découverte normative par page reste ouverte lorsque la recherche n'est pas concluante.
5. **Contrôles distants.** Le nouvel état d'environnement observé est la révision 38, politique HTTP désirée unrestricted mais état d'application unknown. Les requêtes effectives aux API française et anglaise renvoient toujours HTTP 403 le 21 octobre. L'existence du logo et des débats connexes cibles ne peut donc pas être attestée par ces réponses. Le fichier Commons de la carte a des métadonnées consultables mais n'est pas validé comme état juridique actuel : carte datée et contestations à conserver dans la revue.
6. **Références françaises résiduelles.** Les deux liens historiques intégrés aux résumés ne sont pas convertis en fausses références anglaises. Aucun titre d'édition n'est traduit librement. Leur traitement documentaire doit rester explicite et ne pas conduire à réécrire le résumé français.

La convergence sémantique officielle n'a pas été lancée sur un faux état final. Le paquet n'est ni `ready_for_publication` ni `validated`.

## Conservation et reprise

Le paquet conserve les références, les propres notes de lecture, les URL consultées, leurs dates et empreintes, les audits, le corpus source et les fichiers natifs nécessaires à la reprise. Les réponses HTTP intégrales et PDF restent dans le répertoire de recherche local ; ils ne sont pas redistribués dans GitHub ou dans ce paquet.

Ne publier aucune page wiki, ne réutiliser aucun relais français pour l'anglais, ne fusionner ni la branche de livraison ni `wiki-fr-publication` dans `main`, et ne modifier/publier aucun environnement. Aucun reset, nettoyage ou écrasement n'a été réalisé. Les copies interrompues et les commits antérieurs sont conservés.
