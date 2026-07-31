# Migration vers le kit 2.1.17

1. Depuis le kit 2.1.16, déposer l’archive complète dans `updates/` et lancer exceptionnellement `./wikidebia update --no-git` afin que l’ancien gestionnaire ne crée aucun commit avant l’installation du garde-fou 2.1.17.
2. Le modèle `.gitignore` sécurisé est restauré avant tout commit.
3. Les fichiers locaux sensibles déjà suivis sont retirés de l’index avec conservation de leur copie locale.
4. Un push ne demande plus de nom d’utilisateur ou de mot de passe dans le terminal. En l’absence d’authentification, le commit reste local et un message indique d’utiliser GitHub CLI.
5. Après `gh auth login` et `gh auth setup-git`, lancer `./wikidebia github-sync`. Cette commande nettoie l’index, crée le commit de mise à jour resté en attente, puis pousse la branche.
6. La suppression d’un secret de l’historique public reste une opération séparée avec `git filter-repo`.
