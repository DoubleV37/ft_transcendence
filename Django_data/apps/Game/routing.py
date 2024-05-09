from django.urls import path , re_path
from . import consumers

websocket_urlpatterns = [
	re_path("wss/game/solo" , consumers.SoloPongConsumer.as_asgi()) ,
]


