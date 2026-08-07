# Migration de validation vers 1.2.27

Le validateur 0.4.29 accepte les paquets rendus par le kit 2.10.0. Les pages françaises doivent contenir exactement leur lien interlangue anglais verrouillé. Les modèles `Citation` sont comparés aux verrous : seuls `citation` et `date` peuvent différer entre langues, les autres paramètres restent identiques et l’avertissement `Quote translated by AI` est obligatoire en anglais.

Le kit 2.15.0 réutilise ces contrôles pour sceller localement les corpus rendus ; aucune règle de validation supplémentaire n’est introduite.
