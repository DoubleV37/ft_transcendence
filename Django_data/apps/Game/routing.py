from django.urls import path , re_path
from . import consumers , consumers_matchmaking , consumers_multiplayer

websocket_urlpatterns = [
	re_path("wss/game/solo" , consumers.SoloPongConsumer.as_asgi()) ,
	re_path("wss/game/matchmaking" , consumers_matchmaking.MatchmakingPongConsumer.as_asgi()) ,
	re_path(r'wss/game/(?P<room_name>\w+/)$' , consumers_multiplayer.MultiPongConsumer.as_asgi()) ,
]


