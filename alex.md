nachem ich nun vieles schon gemacht hatte, ab heute ale steps:



 2023-12-07

- Freundschaftsanfragen zurückziehen implementiert
- status-field mit statusanzeigen in Friendship-Modell eingebaut für spätere funktionen, die status nutzen könnten
- Profile-edit um das Interessen-Field ergänzt
- die funktion remove_friend im except verändert, dass es nicht alle Errors handelt sondern nur Friendship.DoesNotExist und dann auf profil_detail zurückleitet, wenn nicht existent
-
