# Publier depuis Codex avec les accès MediaWiki de Debian

Le relais permet à Codex de transmettre une demande de publication française par
Git, sans SSH, sans API GitHub et sans copier les identifiants du serveur.

1. Le propriétaire demande explicitement la publication de changements précis.
2. Codex prépare les textes avant/après et une demande liée à leurs SHA-256.
3. Codex envoie cette demande sur la branche distincte `wiki-fr-publication`.
4. Le relais Debian lit cette branche chaque minute et vérifie toutes les pages
   avant la première écriture. Il utilise la configuration Pywikibot existante.
5. Le journal local indique le résultat et les révisions des modifications.

Une fusion dans `main` ne déclenche pas de publication. Le minuteur de déploiement
du programme reste inchangé. Le relais de publication est un service distinct,
à installer et activer explicitement une seule fois.

## Activation initiale sur Debian

Après fusion du code du relais dans `main` et récupération sur le serveur,
exécuter **sous `webmaster` sur Debian**, depuis le checkout :

```bash
cd "/home/users/webmaster/files/Wikidéb'IA"
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
bash deploy/install-publication-relay.sh "$PWD"
```

Cette commande effectue un préflight sans écriture puis active le relais et lance
un premier passage. Les demandes explicitement envoyées pourront alors être
publiées. La configuration `private/pywikibot/` reste en place. Le compte wiki
attendu est lu dans `config/wikidebia.local.json`, avec le fichier exemple comme
valeur de repli. Le compte connecté doit correspondre exactement et posséder les
droits d'édition et de renommage ; la balise `chatgpt` doit être disponible.

Le compte Debian doit pouvoir lire la branche Git dédiée ; aucun droit de push
GitHub n'est nécessaire au serveur. Le démarrage automatique après fermeture de
session suppose le gestionnaire utilisateur persistant, déjà installé pour le
déploiement. Aucun changement de Tailscale ou de SSH n'est nécessaire.

## Envoi depuis Codex Cloud

Un dossier de demande contient `request.json` et les fichiers `before/` et `after/`
déclarés. Le schéma est `wikidebia-fr-publication-request-1.0` ; le site est fixé à
`https://fr.wikidebates.org` et la langue à `fr`. Les SHA-256 des textes et de la
demande empêchent une modification silencieuse du paquet. Ils ne constituent pas
une signature d'identité : l'autorisation de transport repose sur les droits Git
de la branche. Seules les personnes autorisées à publier doivent pouvoir y pousser.

Après l'autorisation explicite de l'utilisateur, envoyer le dossier préparé :

```bash
./wikidebia fr-publication-relay --enqueue DOSSIER_DEMANDE \
  --confirm-request-sha256 EMPREINTE_EXACTE
```

Cette commande utilise un dépôt temporaire de données ; elle ne change pas la
branche ou les fichiers de travail du projet. Le push est une avance rapide
normale. Le contenu d'un identifiant de demande déjà utilisé est immuable ; une
nouvelle correction exige un nouvel identifiant.
La branche `wiki-fr-publication` transporte des données : ne pas la fusionner dans
`main` et ne pas créer de PR pour ses demandes. Seul le code du relais fait l'objet
d'une PR normale.

Le relais n'exécute aucun code provenant de la branche de demandes et refuse les
liens symboliques. Seuls les textes de pages de contenu françaises peuvent être
mis à jour ou renommés. Aucune suppression, nouvelle page ou opération anglaise
n'est prise en charge. Les anciennes pages renommées restent des redirections.
Les liens hors du snapshot continuent ainsi de fonctionner.

## Vérification sur Debian

```bash
systemctl --user list-timers wikidebia-publish-fr.timer
journalctl --user -u wikidebia-publish-fr.service -n 80 --no-pager
ls .state/fr-publication-relay/
```

Le fichier `.state/fr-publication-relay/IDENTIFIANT.json` n'indique `completed`
qu'après relecture de toutes les cibles. Le relais n'envoie pas de reçu vers GitHub :
une demande poussée ou un minuteur actif ne prouvent donc pas la publication.
Le journal et le reçu Debian permettent de la confirmer.

Une page modifiée depuis la préparation ou une collision bloque la demande
entière avant les écritures initiales. Une modification tierce pendant l'exécution
arrête la suite ; les modifications déjà effectuées sont journalisées. Il n'y a
pas de transaction multi-pages ni de retour arrière automatique. Un échec réseau
peut être repris au passage suivant ; les renommages déjà effectués sont reconnus
par leurs redirections et leurs contenus. Un conflit éditorial exige une nouvelle
revue ; il n'est pas retenté en boucle.

Après une édition, le relais relit la révision exacte jusqu'à huit fois, avec deux
secondes entre les lectures, pour attendre la visibilité des métadonnées MediaWiki.
L'identifiant, la révision parente, le compte, le résumé, la balise `chatgpt` et le
SHA-256 du contenu doivent tous correspondre. L'édition n'est pas répétée pendant
ces vérifications ; une divergence persistante reste bloquante et son champ est
indiqué dans le journal.

Le reçu conserve aussi la révision renvoyée par chaque édition avant sa relecture.
Lors d'une reprise explicite, une édition interrompue est vérifiée et ajoutée au
journal avant toute nouvelle écriture, sans être répétée. Les anciens reçus qui
n'avaient enregistré que `update_requested` sont conservés : le relais vérifie
alors la révision courante et sa révision parente avant de poursuivre.

Après diagnostic et résolution d'un conflit, une reprise explicite est possible :

```bash
./wikidebia fr-publication-relay --execute --retry IDENTIFIANT
```

Pour suspendre le relais, arrêter d'abord le minuteur puis laisser finir le passage
en cours avant une autre opération éditoriale :

```bash
systemctl --user stop wikidebia-publish-fr.timer
systemctl --user is-active wikidebia-publish-fr.service
```

Le relais et le déploiement partagent un verrou empêchant leur exécution simultanée.
Les autres commandes éditoriales du projet ne prennent pas ce verrou : ne pas les
exécuter simultanément avec le relais. Aucune manipulation du stash, des corpus
ou des secrets existants n'est effectuée par l'installation.
