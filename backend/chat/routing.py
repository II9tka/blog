from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:room_name>/', ChatConsumer.as_asgi()),
]
