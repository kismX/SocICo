import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message, Room
##
from accounts.models import Profile

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

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        print(data)

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

    @sync_to_async
    def save_message(self, username, room, message):
        user = get_user_model().objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'online_user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        print('Status',data)

        username = data['username']
        connection_type = data['type']

        await self.change_online_status(username, connection_type)
        
    async def send_status(self, event):
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']

        await self.send(text_data=json.dumps({
            'username':username,
            'online_status':online_status,
        }))

    @database_sync_to_async
    def change_online_status(self, username, connection_type):
        user = get_user_model().objects.get(username=username)
        userprofile = Profile.objects.get(user=user)

        print("Account:", userprofile)

        if connection_type == 'open':
            userprofile.chat_status = True
            userprofile.save()

        else:
            userprofile.chat_status = False
            userprofile.save()