# CHAT-APP
#### Erklärungen und Schritt für Schritt Anleitung.

Folgendes muss vorab installiert werden:

```
pip install channels
pip install daphne
```
### Channels:

https://channels.readthedocs.io/en/latest/introduction.html

Channels umhüllt die native asynchrone Ansichtsunterstützung von Django und ermöglicht es Django-Projekten, nicht nur mit HTTP, sondern auch mit Protokollen umzugehen, die langlaufende Verbindungen erfordern - WebSockets, MQTT, Chatbots, Amateurfunk und mehr.

### Daphne:
Daphne ist ein HTTP-, HTTP2- und WebSocket-Protokollserver für ASGI und ASGI-HTTP, der entwickelt wurde, um Django Channels zu betreiben.
____


## ASGI und WSGI

### WSGI
"Web Server Gateway Interface"
- Standard Interface das uns erlaubt, Servercode von unserem Anwendungscode zu trennen
- händelt "requests" und "responses" eins nach dem anderen (daher "synchron")
- kann keine Websockets händeln
    - einige WSGI frameworks: bottle, flask, django
    - einige WSGI server: gunicorn, apache


### ASGI
"Asynchronous Server Gateway interface"
- für Seiten mit einer länger laufenden Verbindung wie z.B Chatrooms
- "asynchron" = requests können in verschiedener ordung ausgeführt werden, auch gleichzeitig!

___

### Zurück  zu Channels:

#### Scopes und Events:

Channels und ASGI teilen eingehende Verbindungen in zwei Komponenten auf: einen <strong>Scope</strong> und eine Reihe von <strong>Events</strong>.

Der Scope ist eine Sammlung von Details über eine einzelne eingehende Verbindung - wie z. B. der Pfad, von dem aus eine Webanfrage gestellt wurde, oder die IP-Adresse, von der ein WebSocket ausgeht, oder der Benutzer, der einen Chatbot anspricht. Der Scope bleibt während der gesamten Verbindung bestehen.

Bei HTTP bleibt der Scope nur für eine einzige Anfrage bestehen. Bei WebSockets bleibt er für die Lebensdauer des Sockets bestehen (ändert sich aber, wenn der Socket geschlossen und neu verbunden wird). Bei anderen Protokollen hängt er davon ab, wie die ASGI-Spezifikation des Protokolls geschrieben ist. So ist es beispielsweise wahrscheinlich, dass ein Chatbot-Protokoll einen Scope für die gesamte Dauer der Konversation eines Benutzers mit dem Bot offen hält, selbst wenn das zugrunde liegende Chat-Protokoll zustandslos ist.

Während der Lebensdauer dieses Scopes treten eine Reihe von Events auf. Diese stellen Benutzerinteraktionen dar, z. B. das Stellen einer HTTP-Anfrage oder das Senden eines WebSocket-Frames. Ihre Channels oder ASGI-Anwendungen werden einmal pro Scope instanziiert und dann mit dem Ereignisstrom gefüttert, der in diesem Scope stattfindet, um zu entscheiden, welche Aktion ausgeführt werden soll.

Ein Beispiel mit HTTP:

    1. Der Benutzer stellt eine HTTP-Anfrage.

    2. Wir öffnen einen neuen Scope vom Typ "http" mit Angaben zum 
    - Pfad, 
    - zur Methode, 
    - zu den Headern usw. der Anfrage.

    3. Wir senden ein http.request-Ereignis mit dem Inhalt des HTTP-Bodys.

    4. Die Channels- oder ASGI-Anwendung verarbeitet dies und erzeugt ein http.response-Ereignis, das an den Browser zurückgesendet und die Verbindung geschlossen wird.

    5. Die HTTP-Anfrage/Antwort ist abgeschlossen und der Scope wird zerstört.

Während der Lebensdauer eines Scopes - sei es ein Chat, eine HTTP-Anfrage, eine Socket-Verbindung oder etwas anderes - gibt es eine Anwendungsinstanz, die alle Ereignisse aus dem Scope verarbeitet. Man kann auch Dinge auf der Anwendungsinstanz speichern. 
Wir könnten unsere ASGI-Anwendung selbst schreiben jedoch gibt uns Channels eine einfach zu nutzende Abstraktion, die so genannten <strong>Consumer</strong>.

#### Consumer

Ein Consumer ist die Grundeinheit des Channels-Codes. Wir nennen ihn Consumer, da er Ereignisse konsumiert, aber Sie können ihn als eine eigene kleine Anwendung betrachten. Wenn eine Anfrage oder ein neuer Socket eintrifft, folgt Channels seiner Routing-Tabelle - die wir uns gleich ansehen werden - um den richtigen Consumer für die eingehende Verbindung zu finden und eine Kopie davon zu starten.

Das bedeutet, dass Consumer im Gegensatz zu Django-Views langlebig sind. Sie können auch kurz laufen - schließlich können HTTP-Anfragen auch von Consumern bedient werden - aber sie sind auf der Idee aufgebaut, für eine Weile zu leben (sie leben für die Dauer eines Scopes, wie wir oben beschrieben haben).

#### Routing

Consumer sind zwar gültige ASGI-Anwendungen, aber wir wollen nicht nur eine schreiben und nur diese an Protokollserver wie Daphne weitergeben. Channels bietet <strong>Routing-Klassen</strong>, die es uns erlauben, unsere Consumer (und jede andere gültige ASGI-Anwendung) zu kombinieren und zu stapeln, um sie je nach Verbindungsart zu versenden.

##### wichtig:
Channels-Router arbeiten nur auf der Scope-Ebene, nicht auf der Ebene der einzelnen Ereignisse, was bedeutet, dass Sie nur einen Consumer für eine bestimmte Verbindung haben können. Das Routing dient dazu, herauszufinden, welcher einzelne Consumer einer Verbindung zugeordnet werden soll, und nicht, wie die Ereignisse einer Verbindung auf mehrere Consumer verteilt werden können.

Router an sich sind gültige ASGI-Anwendungen, und es ist möglich, sie zu verschachteln. Wir schlagen vor, einen ProtocolTypeRouter als Wurzelanwendung des Projekts haben - der, den Sie an Protokollserver weitergeben - und andere, protokollspezifischere Router darin verschachteln.

Channels erwartet, dass wir in der Lage sind, eine einzige Root-Anwendung zu definieren und den Pfad zu dieser als ASGI_APPLICATION-Einstellung bereitzustellen. Es gibt keine feste Regel, wo das Routing und die Root-Anwendung ablegt werden müssen, aber es wird empfohlen, die Konventionen von Django zu befolgen und sie in eine Datei auf Projektebene namens asgi.py zu legen, neben urls.py.

____


## Anleitung zur Chatapp

### 1.  main-project > settings.py

Hier fügen wir unsere Installationen und ASGI application hinzu:
```python
    INSTALLED_APPS = [
        'daphne',   # neu
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'channels', # neu
        'chats', # neu (unsere App in der wir arbeiten werden)
    ]

    WSGI_APPLICATION = 'socico.wsgi.application'
    ASGI_APPLICATION = 'socico.asgi.application'
```
Wir wissen nun dass daphne eine Serveranwendung ist, daher muss sie am Anfang ausgeführt werden und steht daher ganz oben in der Liste.

Danach müssen wir noch die Channellayer festlegen:

```python
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer'
        }
    }
```
Channellayer sind für die Kommunikation zwischen verschiedenen Teilen der Anwendung zuständig. Ein Channellayer ist der "Transportmechanismus" der es mehreren Consumern ermöglicht miteinander und mit anderen Teilen von Django zu kommunizieren.
##### InMemoryChannelLayer:
Für das lokale Speichern des chats 
-> nicht für Produktionsphase empfohlen!

Es gibt einen von Django offiziell unterstützten Channellayer für Produktion der Redis nutzt:
Dafür muss man 
```
'channels_redis'
```

 installieren. Anbei ein Beispiel bei dem Redis auf dem localhost mit entsprechendem Port läuft:

 ```python
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }
 ```

### 2. chats > models.py

class Rooms erstellt:
```python
    class Room(models.Model):
        name = models.CharField(max_length=255)
        slug = models.SlugField(unique=True)
```
##### Slug:
Eine Beschreibung in der URL die nur Buchstaben, Bindestriche, Zahlen oder Unterstriche verwendet.
Beispiel:

w3schools.com/django/learn-about-slug-field

"learn-about-slug-field" <--- ist der Slug

### 3. chats > admin.py
Rooms registriert und Beispielchats im Admin Interface angelegt
```python
    from django.contrib import admin
    from .models import Room

    admin.site.register(Room)
```

### 4. chats > views.py
def rooms() um alle Räume anzuzeigen (ähnlich der ListView)

def room() um einen Raum rauszufiltern:

Wir holen uns den Slug aus unserem Model und vergleichen ihn mit allen Raumobjects dann, returnen wir den entsprechenden Raum
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'chats/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)

    return render(request, 'chats/room.html', {'room': room,})
```

### 5. templates > chats
room.html für einzelne Chaträume und
rooms.html für eine Liste alle Chaträume hinzugefügt

### 6. chats > urls.py 

```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.rooms, name='rooms'),
        path('<slug:slug>/', views.room, name='room'),
    ]
```
In path wird zuerst der gesuchte Datentyp angegeben (wie z.B int), nach dem : kommt dann der Parametername und da wir in views.py in der def room() 'slug' geschrieben haben müssen wir es hier genauso angeben.

### 7. chats > consumers.py

```python
    import json
    from channels.generic.websocket import AsyncWebsocketConsumer
    from asgiref.sync import sync_to_async
    from django.contrib.auth import get_user_model
    from .models import Message, Room

    class ChatConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

        async def disconnect(self, code):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

```

##### from channels.generic.websocket import AsyncWebsocketConsumer
- Class die wir nutzen um den Consumer zu erstellen
##### from asgiref.sync import sync_to_async
- um Sachen in der database der asynchronen view zu speichern
#### connect():
##### self.room_name = self.scope['url_route']['kwargs']['room_name']
- wir wollen anhand der Url den Raumnamen herausfinden
- Consumer erhalten den 'Scope' der Verbindung wenn sie aufgerufen werden mit vielen informationen (wie beim request object)
##### self.room_group_name = 'chat_%s' % self.room_name
- wir vergeben den Namen für unseren Raum also 'chat_' + room.name
##### await self.channel_layer.group_add()
- um dem Channel beizutreten
- async hat das await keyword welches uns erlaubt funktionen zu schreiben die pausiert und später weiter ausgeführt werden können
    - ##### group_add(gruppe, channel)
    - nimmt einen Channel und fügt ihn der Gruppe hinzu wie angegeben. wenn der Channel schon in der gruppe ist macht es ein einfaches return

##### await self.accept()
- wir sind jetzt authentifiziert und connected

#### disconnect():
- zum disconnecten, trennt die Verbindung

### 8. chats > routing.py

```python
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
```
ws => "websocket"
Wir holen uns den Consumer den wir vorher erstellt haben und geben die Url für unseren wWbsocket weiter mit dem Raumnamen als string.

### 9. main_project > asgi.py

```python
    import os
    from django.core.asgi import get_asgi_application
    ### neue imports:
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    from chats.routing import websocket_urlpatterns

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socico.settings')

    # vorher:
    # application = get_asgi_application()
    # neu:
    application = ProtocolTypeRouter({      
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    })
```
#### ProtocolTypeRouter

Sendet an an eine von vielen ASGI applications basierend auf dem Typ der im Scope definiert ist:
- Protokolle definieren einen fixen value typ den der Scope enthält (so kann man zwischen verschiedenen connection typen unterscheiden)
- nimmt nur ein dictonary als input bei dem die Typnamen zu den ASGI applications gemappt werden

Vereinfacht:
```python
ProtocolTypeRouter({
    "http": some_app,
    "websocket": some_other_app,
})
```

#### URLRouter

Leitet Verbindungen vom Typ "http" oder "websocket" über ihren HTTP-Pfad weiter. Nimmt ein einziges Argument entgegen, eine Liste von Django-URL-Objekten (entweder path() oder re_path())

Wenn Gruppen erfasst werden, werden sie im Scope gespeichert als:
- <strong>key url_route,</strong>
- ein dict mit <strong>kwargs key</strong> welches ein dictionary von regex gruppen enthält,
- und ein <strong>args key</strong> mit einer liste von positional regex Gruppen

um z.B die benannte Gruppe "room_name" zu bekommen (wie in unserer consumers.py) haben wir das geschrieben:

```python
# in consumers.py
    self.room_name = self.scope['url_route']['kwargs']['room_name']
```

#### AuthMiddlewareStack
Für Authentifizierung
- AuthMiddleware 
    - speichert user details in einer Session
- braucht SessionMiddleware und SessionMiddleware braucht 
- CookieMiddleware um zu funktionieren, daher 

<strong>AuthMiddlewareStack</strong> da hier alle 3 enthalten sind.

### 10. HTML Dateien:

#### base.html:

In Main Menü:
```html
    <a href="{% url 'rooms' %}">Chatrooms</a> 
```

Am unteren Ende der Datei:
```script
    {% block scripts %}
    {% endblock scripts %}
```
Hier kommt unser Javascript rein.

#### chats > rooms.html

```html
    {% extends 'base.html' %}

    {% block title %}Chatrooms | {% endblock %}

    {% block content %}

    {% for room in rooms %}
        <div>
            <h2>{{ room.name }}</h2>
            <a href="{% url 'room' room.slug %}">Chat beitreten</a>
        </div>
    {% endfor %}

    {% endblock content%}
```
Zuerst loopen wir durch alle Räume.
Dann haben wir den Link zum beitreten angepasst und übergeben mit room.slug den slug für unsere Url und schließlich unsere funktion.

#### chats > room.html

```html
    {% extends 'base.html' %}

    {% block title %}{{ room.name }} | {% endblock %}

    {% block content %}
        <h1>Aktueller Chat: {{ room.name }}</h1>

    <!-- Teil 1 -->
    {% for message in messages %}
    <div class="chat-messages" id="chat-messages">
            <div>
                <p class="chat-name">{{ message.user.username }}</p>
                <p class="chat-message-box">{{ message.content }}</p>
            </div>
    </div>
    {% endfor %}
    
    <!-- Teil 2 -->
    <div class="chat-form">
        <form method="post" action="." class="flex">
            <input type="text" name="content" class="chat-form-input" placeholder="Deine Nachricht..." id="chat-message-input">

            <button class="chat-form-button" id="chat-message-submit">Senden</button>
        </form>
    </div>
```
#### Teil 1:
Wir fügen ein div ein was das gesammte Fenster unseres Chats darstellt und geben ihm die Klasse und ID "chat-messages".
Darin befinden sich 2 p-tags die später unseren Usernamen und die Nachricht anzeigen sollen. Dazu haben sieauch passende classen bekommen damit wir sie später ansprechen können.

#### Teil 2:
Hier fügen wir unser Formular ein was unsere Eingabe im Chat darstellt. Daher brauchen wir nur ein Textfeld und einen Button zum Senden. Der Input und der Button haben auch entsprechende IDs erhalten damit wir sie später ansprechen können.

### 11. Javascript

Unser Javascript befindet sich in room.html

```html
{% block scripts %}

{{ room.slug|json_script:"json-roomname" }}
{{ request.user.username|json_script:"json-username" }}

<script>
    const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
    const userName = JSON.parse(document.getElementById('json-username').textContent);

    // Websocket Connection:

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function(e) {
        console.log('onmessage')

        const data = JSON.parse(e.data);

        if (data.message){
            let html = '<div>';
                html += '<p class="chat-name">'+ data.username + '</p>';
                html += '<p class="chat-message-box">'+ data.message + '</p></div>';

                document.querySelector('#chat-messages').innerHTML += html;
                scrollToBottom();
        } else {
            alert('Die Nachricht war leer...')
        }
    }

    chatSocket.onclose = function(e) {
        console.log('onclose')
    }

    // Nachricht senden:

    document.querySelector('#chat-message-submit').onclick = function(e){
        e.preventDefault();

        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;

        chatSocket.send(JSON.stringify({
            'message': message,
            'username': userName,
            'room': roomName
        }));

        messageInputDom.value = ''; //zurücksetzen der variable

        return false;
    }

    // Automatisch zum Ende der Nachrichten scrollen:

    function scrollToBottom(){
        const objDiv = document.querySelector('#chat-messages');
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    scrollToBottom(); // um funktion aufzurufen
</script>
{% endblock %}
```

#### Allgemeine Erklärungen zur Javasciptsyntax

#### const chatSocket
- eine lokale variable namens "chatSocket" deren Wert nicht durch Neuzuordnung mit "=" geändert werden kann z.B.: 
```javascript
const num = 1
num = 2
```
---> geht nicht weil num "Konstant" ist
- außer const wird zum objekt, dann können Eigenschaften verändert, hinzugefügt oder entfernt werden

#### new

- lässt uns eine Instanz eines user-definierten Objekttypen oder eines der built-in Objekttypen erstellen, welche eine constructor funktion enthalten ( ähnlich funktionen in python)
z.B.:
```javascript
    function Car(make, model, year) {
        this.make = make;
        this.model = model;
        this.year = year;
    }

    const car1 = new Car('Eagle', 'Talon TSi', 1993);

    console.log(car1.make);
    // Expected output: "Eagle"
```
____

#### Websocket Connection:

Wir erstellen const chatSocket und erstellen eine neue Instanz Websocket.
Hierfür Verbinden wir einzelne Elemente um eine URL zu erhalten die auf unseren Server verweist.

Websocket
- Mit dem Websocket Objekt können eine Websocketverbindung zum Server erstellen und verwalten. Außerdem können wir Daten hiermit senden und empfangen.

'ws://'

- wss verbindet nur mit https
- ws verbindet nur mit http

window.location.host

- flexible Angabe der aktuellen IP plus Port
- wie als würden wir "127.0.0.1:8000" schreiben

'/ws/'

- der Pfad den wir in den websocket-urlpatterns angegeben haben

roomName

- Am Anfang des script-blocks schreiben wir:
```html
{{ room.slug|json_script:"json-roomname" }}
```
hier holen wir unseren Slug und wandeln ihn in ein JSON um mit dem Namen "json-roomname"
Dann:
```javascript
    const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
```
Wir erstellen am Anfang unseres Scripts eine const roomName und dann lesen wir unser JSON objekt aus.

JSON
- Objekt das static methods enthält zum Auslesen von JSON Daten oder zum Konvertieren in JSON 

parse()
- Liest einen String-Text als JSON, transformiert optional den erzeugten Wert und seine Eigenschaften und gibt den Wert zurück.

document.getElementById()
- Die Methode getElementById() der Document-Schnittstelle gibt ein Element-Objekt zurück, das das Element darstellt, dessen id-Eigenschaft mit der angegebenen Zeichenkette übereinstimmt. Da Element-IDs, wenn sie angegeben werden, eindeutig sein müssen, sind sie eine nützliche Methode, um schnell auf ein bestimmtes Element zuzugreifen.
- in unserem Fall ist die "Zeichenkette" -> 'json-roomname'

.textContent
- wandelt unser JSON in einen text um

___

chatSocket.onmessage = function(e){}
- mit onmessage wartet das Programm auf ein Event, bei dem eine Nachricht abgesendet wurde
- wenn dieses Event passiert wird unsere function aufgerufen und die Details des Events als parameter e weitergegeben

console.log('onmessage')
- printet uns eine Nachricht in die Konsole

Wir wandeln nun wieder unsere Daten um in JSON und sagen "(if)wenn eine Nachricht geschickt wird...":

...dann soll in unserem HTML Dokument folgende Objekte unseren Usernamen (data.username) und unsere Nachricht (data.message) enthalten.
Mit dem document.querySelector() wählen wir unsere komplette Chatbox und fügen dieser unsere Änderungen hinzu (innerHTML + html). Dann lösen wir unsere funktion scrollToBottom() aus (dazu später mehr).

"(else) wenn die Nachricht leer ist..."

...kriegen wir einen Alert

chatSocket.onclose = function(e){}
- wenn unsere Verbindung geschlossen wird printet er wieder in die Konsole
___

#### Nachricht senden

```javascript
document.querySelector('#chat-message-submit').onclick = function(e){...}
```
Zuerst wählen wir unseren Button mit der ID '#chat-message-submit' und sagen onclick() also wartet das Programm wieder darauf dass dieses Event ausgelöst wird (wir also den Button "klicken") um die funktion darauf auszuführen.

preventDefault();
- teilt unserer Funktion mit, dass die Standardaktion nicht wie üblich ausgeführt werden soll, wenn das Ereignis nicht ausdrücklich behandelt wird.
- Das bedeutet dass man Aktionen manipulieren kann da das Programm sich nicht weiter daran aufhängt wenn du nichts ausdrücklich beschrieben hast

Beispiel:
onclick wird auch für checkboxes genutzt. Wenn wir nun aber sagen "wenn gelickt wird" (onclick) dann führ preventDefault() aus, ist die Box zwar klickbar aber ihr natürliches vordefiniertes Verhalten wird verändert indem sich das aussehen der Box nicht verändert und sie auch nicht anwählbar wird (mehr dazu hier https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault)

Danach erstellen wir 2 const, zuerst holen wir uns unser Element  im HTML was unsere Nachricht enthät und dann extrahieren wir den Wert daraus.

```javascript
chatSocket.send(JSON.stringify({
            'message': message,
            'username': userName,
            'room': roomName
        }));
```
.send()
- Die Methode WebSocket.send() stellt die angegebenen Daten in die Warteschlange, die über die WebSocket-Verbindung an den Server übertragen werden sollen. Wenn die Daten nicht gesendet werden können, wird der Socket automatisch geschlossen.
- Wenn Sie send() aufrufen, wenn sich die Verbindung im Zustand CLOSING oder CLOSED befindet, verwirft der Browser die Daten stillschweigend.

JSON.stringify()
- Gibt eine JSON-String zurück, der dem angegebenen Wert entspricht und optional nur bestimmte Eigenschaften enthält oder Eigenschaftswerte auf eine benutzerdefinierte Weise ersetzt.

#### Automatisch zum Ende der Nachrichten scrollen

```javascript
    function scrollToBottom(){
        const objDiv = document.querySelector('#chat-messages');
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    scrollToBottom();
```
Wir erstellen eine Funktion namens "scrollToBottom". Darin holen wir uns unsere komplette Chatbox und sagen dann:

objDiv.scrollTop = objDiv.scrollHeight;

.scrollTop
- Die Eigenschaft Element.scrollTop ruft die Anzahl der Pixel ab, um die der Inhalt eines Elements vertikal gescrollt wird, oder legt diese fest.
- Der scrollTop-Wert eines Elements ist ein Maß für den Abstand zwischen dem oberen Rand des Elements und seinem obersten sichtbaren Inhalt. Wenn der Inhalt eines Elements keinen vertikalen Scrollbalken erzeugt, ist sein scrollTop-Wert 0.
- unser Scrollbalken wird im CSS erzeugt

.scrollHeight
- Die Eigenschaft Element.scrollHeight misst die Höhe des Inhalts eines Elements, einschließlich des Inhalts, der aufgrund von Überlauf nicht auf dem Bildschirm sichtbar ist.

Danach rufen wir die Funktion scrollToBottom() einfach auf, da sie ja gleich beim laden der Seite ausgeführt werden soll.
Wir rufen sie auch beim Senden von Nachrichten auf, da wir ja nach dem senden gleich automatisch nach unten gescrollt wrden wollen.

### 12. chats > consumers.py

In "ChatConsumer" kommt nun folgendes dazu:

```python
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'room': room,
        }))
```
receive(self, text_data)
- text_data ist der JSON string den wir erstellt haben in room.html
- wir ziehen uns die werte des dictonary aus dem javascript von chatSocket.send()
- diese funktion greift sich die Infos der Nachricht und verarbeitet sie weiter fürs senden

chat_message():
- formatiert das JSON der Nachriht in einen String mit json.dumps()

### 13. chats > models.py

```python
class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
```
Wir wollen unsere Nachrichten in der Datenbank speichern daher brauchen wir das model Message.

### 14. chats > views.py

```python
@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room) #neu

    return render(request, 'chats/room.html', {'room': room, 'messages': messages}) #neu
```
- def room() angepasst mit messages Variable um die Nachrichten des entsprechenden Raums herauszufiltern
- dann im return geben wir unsere Nachrichten wieder aus

### 15. chats > consumers.py

In ChatConsumer fügen wir noch folgendes hinzu:
```python
@sync_to_async
    def save_message(self, username, room, message):
        user = get_user_model().objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)
```
@sync_to_async 
- macht es möglich Sachen in der Datenbank zu speichern während wir "await" benutzen -> sozusagen speichern wir und "warten" bis es fertig ist

def save_message():
- wir holen uns den User und den Raum anhand des Slug aus dem Frontend
- dann erstellen wir ein neues Message object um unseren usernamen, room und die Nachricht zu speichern

Wir müssen diese Funktion nun aufrufen wenn eine Nachricht reinkommt daher fügen wir unsere Funktion in def receive() hinzu:

```python
async def receive(self, text_data):
        ...
        await self.save_message(username, room, message)
        ...
```

Wir geben hier unseren usernamen, room und die nachricht rein die wir über "data" definiert haben