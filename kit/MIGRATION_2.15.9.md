# Migration vers le kit 2.15.9

Le kit 2.15.9 s'aligne sur la norme 1.2.34 et le validateur 0.4.36. Pour publier uniquement le français, déclarer `translation_status.en=deferred`, employer le profil `norm_1_2_deferred_translation` et ne produire aucun lien interlangue. Après traduction, passer à `ready`, publier l'anglais, puis utiliser l'exemple `configs/reprise_interlangue_1.2.34.example.json` pour enrichir le français.
