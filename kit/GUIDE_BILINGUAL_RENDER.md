# Rendu bilingue déterministe

```bash
./wikidebia corpus-workspace-render <debate_id> --work-id <work_id> --confirm-translation-sha256 <sha256>
```

La commande crée `rendered-copy/`, rend les pages françaises et anglaises, ajoute un lien interlangue direct à chaque page française, rend les citations verrouillées, verrouille le graphe et exécute la validation complète. Elle n’effectue aucun accès distant ni aucune publication.
