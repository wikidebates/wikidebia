# Migration Kit 2.15.53 — paramètres `sujet-développé` et `débat-dédié`

Le rendu courant émet `sujet-développé` / `expanded-topic` et `débat-dédié` / `dedicated-debate`. Les anciennes formes restent reconnues à l'import et à la reprise des corpus antérieurs, puis sont normalisées vers les nouveaux noms sans altération de valeur. Les options de parcours exposent désormais `--follow-local-relations-at-dedicated-debate`; l'ancien nom de l'option reste un alias CLI de compatibilité.
