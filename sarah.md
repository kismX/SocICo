1. installed channels
2. ´´´ pip install channels´´´
3. tailwind css in base.html eingefügt und vorerst auskommentiert
4. in main settings.py :
   WSGI_APPLICATION = 'socico.wsgi.application'
   ASGI_APPLICATION = 'socico.asgi.application'

   wsgi -> Web Server Gateway Interface

   -> standart interface das uns erlaub server code von unserem anwendungscode zu trennen
   -> händeln requests und responses eins nach dem anderen (daher "synchron")
   -> einige wsgi frameworks: bottle, flask, django
   -> einige wsgi server: gunicorn, apache
   -> kann keine websockets händeln

   asgi -> Asynchronous Server Gateway interface
   -> für seiten mit einer länger laufenden verbindung wie z.b chats
   -> "asynchron" = requests können in verschiedener ordung ausgeführt werden, auch gleichzeitig!
5. in chats > models.py
   class ChatRooms erstellt
   -> Slug:
   eine bescreibung in der URL die nur buchstaben, bindestriche, zahlen oder unterstriche verwendet.
   z.B w3schools.com/django/learn-about-slug-field
   "learn-about-slug-field" ist der Slug
6. in chats > admin.py
   ChatRooms registriert, Beispielchats im admin interface angelegt
7. liste der chaträume in html hinzugefügt
8. in chats > views.py
   def chat_detail hinzugefügt um einzelnen chat anzuzeigen
   wir holen uns den slug aus unserem model und vergleichen ihn mit unseren objects dann returnen wir den entsprechenden raum
9. templates > room.html hinzugefügt
10. chats > urls.py angepasst
    in path wird zuerst der gesuchte datentyp angegeben (wie z.B int), nach dem : kommt dann der parameter name und da wir in views.py in der def chat_detail() 'slug' geschrieben haben müssen wir es hier so angeben
11. templates > chatroom.html
    hier haben wir den link zum beitreten angepasst und übergeben mit room.slug den slug für unsere url und schließlich unsere funktion
    templates > room.html
    form zum senden der nachricht eingefügt
12. in socico settings.py

    CHANNEL_LAYERS =
    {'default':
    {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}

    -> channellayer sind für die kommunikation zwischen verschiedenen teilen der anwendung zuständig. Ein Channellayer ist der "Transportmechanismus" der es mehreren consumern ermöglicht mit einander und mit anderen teilen von django zu kommunizieren.
    ->InMemoryChannelLayer:
    für das speichern des chats local -> nicht für produktionsphase empfohlen!
    es gibt einen von django offiziell unterstützten channel layer für produktion der Redis nutzt:
    dafür muss man 'channels_redis' installieren. Anbei ein Beispiel bei dem Redis auf dem localhost mit entsprechendem Port läuft:

    ```
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }
    ```
13. chats > consumers.py
    from channels.generic.websocket import AsyncWebsocketConsumer
    -> Class die wir nutzen um den Consumer zu erstellen
    from asgiref.sync import sync_to_async
    -> um sachen in der database der asynchronen view zu speichern
    in connect():
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    -> wir wollen anhand der url den raumnamen herausfinden
    -> consumer erhalten den 'scope' der verbindung wenn sie aufgerufen werden mit vielen informationen (wie beim request object)
    ---> also ist ein scope der ort wo connection infos zu finden sind und an dem die middleware attribute hinzufügen kann (immernoch wie beim request)
    self.room_group_name = 'chat_%s' % self.room_name
    -> wir vergeben den namen für unseren raum also 'chat_' + room.name
    await self.channel_layer.group_add()
    -> um dem channel beizutreten
    -> async hat das await keyword welches uns erlaubt funktionen zu schreiben die pausiert und später weiter ausgeführt werden können
    ----> group_add(gruppe, channel)
    -> nimmt einn channel und fügt ihn der gruppe hinzu wie angegeben. wenn der channel schon in der gruppe ist macht es ein einfaches return

    await self.accept()
    -> wir sind jetzt authentifiziert und connected

    async def disconnect():
    -> zum disconnecten, trennt die verbindung
14. chats > routing.py

    websocket_urlpatterns = [

    path('ws/<[str:room_name](str:room_name)/', consumers.ChatConsumer.as_asgi()),

    ]
    -> ws steht für websocket
15. socico > asgi.py
    Imports:

    ---

    application = get_asgi_application()
    wurde ersetzt durch:
    application = ProtocolTypeRouter({

    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
    URLRouter(
    chats.routing.websocket_urlpatterns
    ))})
    ---------->


    ```
    ProtocolTypeRouter({
        "http": some_app,
        "websocket": some_other_app,
    })
    ```
    sendet an an eine von vielen ASGI applications basierend auf dem typ der im scope definiert ist
    -> protokolle definieren einen fixen value typ den der scope enthält (so kann man zwiscen verschiedenen connection typen unterscheiden)
    -> nimmt nur ein dictonary als input bei dem die typ namen zu den asgi applications gemappt werden
    ------->
    URLRouter:
    -> Leitet Verbindungen vom Typ http oder websocket über ihren HTTP-Pfad weiter. Nimmt ein einziges Argument entgegen, eine Liste von Django-URL-Objekten (entweder path() oder re_path())
    -> wenn gruppen erfasst werden, werden sie im scope gespeichert als:
    key url_route,
    ein dict mit kwargs key welches ein dictionary von regex gruppen enthält,
    und ein args key mit einer liste von positional regex gruppen
    um z.B die benannte gruppe "stream" zu bekommen müssten wir das schreiben:

    ```
    stream = self.scope["url_route"]["kwargs"]["stream"]
    ```
16. 
17.
