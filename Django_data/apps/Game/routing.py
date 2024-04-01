from django.urls import path , re_path
from . import consumers , consumers_matchmaking

websocket_urlpatterns = [
	path("wss/game/solo" , consumers.SoloPongConsumer.as_asgi()) ,
	path("wss/game/matchmaking" , consumers_matchmaking.MatchmakingPongConsumer.as_asgi()) ,
	re_path(r'wss/game/(?P<room_name>\w+)/$' , consumers.MultiPongConsumer.as_asgi()) ,
]


