# Migration 2.16.45 — changement de jour pendant la publication finale

Aucune migration manuelle de `.state/` n'est requise.

Lorsqu'une publication finale partiellement exécutée sous un plan du jour précédent est reprise, le kit 2.16.45 relit les pages anglaises distantes et construit un plan successeur audité. Les pages déjà créées gardent leur date de création réelle ; les pages encore absentes reçoivent le jour courant au moment de leur création.

Ne supprimez ni `authorization.json`, ni les plans, ni les journaux de la publication interrompue : ils constituent la preuve nécessaire à la reprise.
