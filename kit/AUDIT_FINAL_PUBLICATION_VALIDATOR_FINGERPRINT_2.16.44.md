# Audit — empreinte du validateur en publication finale — kit 2.16.44

Le chemin `final_publication` construit trois configurations distantes. Le plan anglais utilise `GenericPublisher`, dont le scellement appelle `_package_fingerprints()` et exige `validator.fingerprint_path`. Jusqu’en 2.16.43, `_common_remote()` omettait ce champ, d’où un `KeyError` avant l’autorisation de toute écriture distante.

2.16.44 ajoute explicitement le chemin du composant validateur installé et `max_warnings=0`. Une régression instancie le `GenericPublisher` depuis `_english_config()` et exécute le calcul des empreintes. Aucun contenu éditorial ni état de publication n’est migré.
