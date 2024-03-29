from django.urls import path , re_path
from . import consumers

websocket_urlpatterns = [
	path("wss/game/solo" , consumers.SoloPongConsumer.as_asgi()) ,
	path("wss/game/matchmaking" , consumers.MatchmakingPongConsumer.as_asgi()) ,
	re_path(r'wss/game/(?P<room_name>\w+)/$' , consumers.MultiPongConsumer.as_asgi()) ,
]


