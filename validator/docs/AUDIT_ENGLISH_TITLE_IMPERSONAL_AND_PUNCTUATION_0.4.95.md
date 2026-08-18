# Audit — titres anglais — validateur 0.4.95

Le blocage réel `revenu_de_base` a révélé deux catégories distinctes. A0026 et A0028 commencent par `It is unfair for … to …` : `It` est extraposition impersonnelle, le sujet logique est la proposition infinitive qui suit et aucun référent extérieur n’est requis. Le contrôle a été resserré pour exempter uniquement les constructions où cette proposition est syntaxiquement visible.

D’autres titres contenaient l’apostrophe typographique `’`. La norme 1.2.87 exige l’apostrophe droite ASCII `'` dans les possessifs et contractions des titres. Le validateur rejette désormais explicitement les principales variantes typographiques non ASCII.

Régressions : extraposition positive, pronom anaphorique négatif, cas ambigu `It is harmful to democracy`, et apostrophe typographique après verrou anglais.
