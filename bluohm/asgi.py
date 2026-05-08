import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bluohm.settings")

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import messaging.routing


application = ProtocolTypeRouter({

    # Traditional Django HTTP
    "http": django_asgi_app,

    # WebSocket support
    "websocket": AuthMiddlewareStack(
        URLRouter(
            messaging.routing.websocket_urlpatterns
        )
    ),
})
