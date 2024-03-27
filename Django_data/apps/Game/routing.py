from django.urls import path , include
from .consumers import PongConsumer

websocket_urlpatterns = [
    path("wss/game/room" , PongConsumer.as_asgi()) ,
]
