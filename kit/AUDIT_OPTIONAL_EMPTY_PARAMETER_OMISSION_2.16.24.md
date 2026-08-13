# Audit — omission canonique des paramètres optionnels vides — kit 2.16.24

Le mécanisme 2.16.22 `present-empty` transformait la présence historique d’un paramètre en obligation de conserver une ligne vide. Sur le vote électronique, cela produisait notamment `|bibliographie-pour=`, `|vidéographie-contre=` et `|objections=`.

Le contrat 2.16.24 conserve `source_parameter_presence` uniquement pour l’audit, omet toute valeur éditoriale optionnelle vide et autorise cette omission au préflight uniquement pour le jeu fermé des paramètres éditoriaux optionnels gérés. Les paramètres protégés, inconnus et hors contrat restent soumis à la barrière de suppression.
