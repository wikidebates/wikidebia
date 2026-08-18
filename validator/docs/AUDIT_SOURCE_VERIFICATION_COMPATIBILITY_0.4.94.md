# Audit — compatibilité des vérifications documentaires — validateur 0.4.94

Le schéma précédent exigeait un booléen `verification.primary_source` même pour un paquet de traduction déjà préparé par le kit avec l'ancien format `checked_at` / `method` / `note`, qui n'enregistrait aucune classification primaire/secondaire. Forcer `false` aurait inventé une donnée documentaire.

Le schéma 0.4.94 conserve donc la présence obligatoire de la clé mais admet la valeur `null` uniquement comme représentation explicite de cette information historiquement absente. Les nouvelles revues restent tenues de fournir `true` ou `false`; cette exigence est appliquée par le kit. Les anciennes clés demeurent interdites dans le registre final.
