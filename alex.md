nachem ich nun vieles schon gemacht hatte, ab heute ale steps:



 2023-12-07

- Freundschaftsanfragen zurückziehen implementiert
- status-field mit statusanzeigen in Friendship-Modell eingebaut für spätere funktionen, die status nutzen könnten
- Profile-edit um das Interessen-Field ergänzt
- die funktion remove_friend im except verändert, dass es nicht alle Errors handelt sondern nur Friendship.DoesNotExist und dann auf profil_detail zurückleitet, wenn nicht existent

2023-12-08

- neue app "searchers" implementiert
- darin in views.py die neue funktion user_finder() implementiert.
- template für user_finder.html erstellt
- Accounts-app - models.py: Profile - Modell um age, gender, location, is_active, und last_online erweitert , um es bei suchen einzubeziehen und anderen funktionalitäten
- accounts-signals.py: user_logged_in_handler und user_logged_out_handler imlementiert, die signal abgreift und in den view zu update_activity_status schickt
- accounts-app - views.py: update_activity_status funktionalität implementiert, die last_online im Profile aktualisieren, wenn user online oder offline geht
- template user_filter.html - für interessen und andere eigenschaften von user-suche erstellt
- template profile_edit.html - neue forms gender, age, ...hinzugefügt
- template base.html - Menü angepasst + Seeek hinzugefügt
- accounts-forms.py: neue profile forms gender, age ...hinzugefügt

9.12.23
- last_online wird korrekt angezeigt bei seeek

10.12.23
- settings.py: TIME_ZONE von UTC auf Europe/Berlin geändert für korrekte Zeitangabe. UTC ist weltzeituhr. die Variable USE_TZ = True sagt, dass man timezones nutzen kann und UTC umgerechnet wird auf die eingestellte, hier also Europe/Berlin
-  man kann mehrere suchbegriffe in komma getrennt in kombination abfragen und bekommt passenden user angezeigt 
