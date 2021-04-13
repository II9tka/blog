from channels.auth import AuthMiddlewareStack
from django.urls import path

from .consumers import ChatConsumer, ChatNotifyConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:room_name>/', ChatConsumer.as_asgi()),
]

http_urlpatterns = [
    path(
        'notifications/', AuthMiddlewareStack(ChatNotifyConsumer.as_asgi()),
    ),
    # path(
    #     'notifications/<int:chat_id>/'
    # )
]
