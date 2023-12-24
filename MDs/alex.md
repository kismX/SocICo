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
- man kann mehrere suchbegriffe in komma getrennt in kombination abfragen und bekommt passenden user angezeigt


11.12.23

- searchers: view und template: man kann ein timedelta in der suchfunktion eingeben nach Tagen, wann ein user zuletzt online war
- searchers: user der suchergebnisse werden nun als links zu den entsprechenden userprofilen angezeigt



12.12.23

- template-ordner searchers etabliert. ausbesserungen, tippfehler (..)

...

21.12.23
- erstellung eines models Terms in searchers-app , um modell zu haben, in welchem words gespeichert werden, die mit einem algorithmus verglichen werden können mit user-sucheinbgaben, um suchvorschläge zu liefern usw. 
    - weiter hat es auch schon ein feld synonyme für die folgende synonym-implementierung
    - und ein Category-Field für verknüfung der wörter mit kategorien
- weiter ein model für kategorien, welches in abhängigkeit zum Term model ist, um später wortkategorien gründen zu können
- installieren von fuzzywuzzy (wörter vergleichen, score machen usw)
- requirements erweitert
- view, urls, forms.py, templates erstellt, die neue wörter aufnimmt oder löscht in liste
- seeek im View "user_filter"  um ähnliche wortvorschläge bei tippfehlern und nicht gefundenen usern erweitert

2023-12-22
- Wörterbuch liste aus term_list bei add_terms integriert, dadurch Templet gespart
- Wörter werden nun seiten weise mit 10 begriffen pro page angezeigt

2023-12-23
- app "posts" integriert
- (die dinge hier sind nicht all zu kompliziert, da nur models erstellt wurden, die infos posten, wie wir es im kurs auch gemacht haben)

- ein model für posts (dass man text, bild, link und event -mit foreign key auf Event-Modell- für event-objekte posten) posten kann
- ein model für events erstennen (titel, beschreibung foto des events usw)
- Views erstellt in Profile_detail um Timeline (mal so genannt) mit eigenen posts auf dem profil sichtbar zu machen
- eine view "home" erstellt, die es biher nicht gab, auf die newsfeed aller user eingehen (sollte noch angepasst werden auf user, die freunde sind, oder denen man folgt oder so)

- eine app "basics" erstellt, um grundlegende dinge hier getrennt von spezifischen apps zu haben.
- view für "home" nun in basics.views integriert, da es hier zentral liegt und nicht versteckt in zb posts.views

2023-12-24
- eigeneposts werden sind nun auf dem userprofil editier- und löschbar.
- weiter kann man nun auf der profilseite auch in einer Form posten anstatt auf einem sepataten create_post template, was komfortabler ist
- auf der home-seite wird nun alles korrekt angezeigt
- die css habe ich bei .main-menu{position: fixed; top: 0;} die position fixed anstatt flexible gemacht, weil die sidebar sichtbar wurde beim scrollen und weil es fixed hochwertiger wirkt, dazu musste ich top: 0 hinzufügen, um die nav ganz oben an die page zu bringen.
- weiter musste ich dann bei .row{margin-top: 150px;} von 50 auf 150px erhöhen, da die fixierte .row sonst teile des bodys überschttete. 

- etwas codew gesäubert an verschiedenen stellen, dinge gelöscht, die niocht gebraucht wurden
- bei geposteten links werden jetzt die domainnamen angezeigt anstatt lediglich ein verlinkter string "Link" 