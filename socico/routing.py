from django.urls import path
from notifications import consumers as notifications_consumer
from chats import consumers as chats_consumer

websocket_urlpatterns = [
    path('ws/notifications/', notifications_consumer.NotificationConsumer.as_asgi()),
    path('ws/online/', chats_consumer.OnlineStatusConsumer.as_asgi()),
    path('ws/<str:room_name>/', chats_consumer.ChatConsumer.as_asgi()),
    
]