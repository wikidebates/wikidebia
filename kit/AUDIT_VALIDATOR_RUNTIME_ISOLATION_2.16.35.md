# Audit — isolation runtime du validateur (2.16.35)

Le diagnostic `render_preflight` du vote électronique sous 2.16.34 déclarait le validateur 0.4.101 mais rapportait encore 164 sous-anomalies de style sur cinq résumés historiques autorisés. Les mêmes `fr_content_lock.json`, `en_content_lock.json` et `summary_style_review.json`, chargés directement par le code 0.4.101 livré, produisent zéro anomalie de style.

Le correctif 2.16.35 traite cette divergence comme un défaut d’identité runtime et non comme une raison d’affaiblir `WDV-EDT-013/014/015/020`. `_run_validator` exécute maintenant le sous-processus depuis `validator/`, avec `PYTHONPATH` exclusivement égal à `validator/src`, `PYTHONNOUSERSITE=1`, `PYTHONDONTWRITEBYTECODE=1` et sans `PYTHONHOME` hérité.

Une régression crée volontairement une fausse copie `wikidebia_validator` dans le répertoire de travail et dans le `PYTHONPATH` hérité ; seule la copie installée sous `validator/src` doit être exécutée.
