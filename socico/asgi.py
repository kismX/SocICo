"""
ASGI config for socico project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socico.settings')
django_asgi_app = get_asgi_application()

### neue imports:
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#from chats.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from . import routing



application = ProtocolTypeRouter({      #kommt von channels + notifications
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
