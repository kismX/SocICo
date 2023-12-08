"""
ASGI config for socico project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
### neue imports:
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chats.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socico.settings')

application = ProtocolTypeRouter({      #kommt von channels
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    )
})
