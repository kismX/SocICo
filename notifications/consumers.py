import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect method aufgerufen") # test
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            # Erstelle n einzigartigen groupname für den User
            self.group_name = f"notification_user_{self.user.id}"
            print(f"Groupname connect: {self.group_name}")
            # Füge user zur Gruppe hinzu
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"WebSocket connected yo. Group: {self.group_name}") #test

    async def disconnect(self, code):
        # Entferne User aus Group, wenn Verbindung getrennt wird
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"WebSocket getrennt. Groupp: {self.group_name}") #test

    async def receive(self, text_data):
        print(f"Nachricht empfangen: {text_data}")  # test
        data = json.loads(text_data)
        notification_id = data.get('notification_id')
        
        # Abrufen / Senden der notification
        notification = await self.get_notification(notification_id)
        if notification:
            notification_data = {
                'type': 'notification',
                'notification_id': notification.id,
                'notification_type': notification.notification_type,
                'notification_info': notification.notification_info,
                'notification_link': notification.notification_link,
            }
            await self.send(text_data=json.dumps(notification_data))

    async def send_notification(self, event):
        print(f"Notification-Event bekommenn: {event}") #test

        # Method wird aufgerufen, wenn Nachricht an group gesendet wird
        notification_message = event['message']
        # Sende notification an den verdammten WebSocket
        await self.send(text_data=json.dumps(notification_message))


    @sync_to_async
    def get_notification(self, notification_id):
        print(f"Notificqation abrufen: {notification_id}") #test

        try:
            return Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return None