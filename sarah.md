1. installed channels
   ´´´ pip install channels´´´
2. tailwind css in base.html eingefügt und vorerst auskommentiert
3. in main settings.py :
   WSGI_APPLICATION = 'socico.wsgi.application'
   ASGI_APPLICATION = 'socico.asgi.application'

   wsgi -> für normale seiten
   asgi -> für seiten mit einer länger laufenden verbindung wie z.b chats
4. in chats > models.py
   class ChatRooms erstellt
   -> Slug:
   eine bescreibung in der URL die nur buchstaben, bindestriche, zahlen oder unterstriche verwendet.
   z.B w3schools.com/django/learn-about-slug-field
   "learn-about-slug-field" ist der Slug
5.
