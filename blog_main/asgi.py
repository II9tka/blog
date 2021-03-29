import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from backend.chat.middleware import TokenAuthMiddlewareStack
from backend.chat.routing import websocket_urlpatterns, http_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_main.settings")

application = ProtocolTypeRouter({
    "http": URLRouter(
        http_urlpatterns +
        [re_path(r'', get_asgi_application())]
    ),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
