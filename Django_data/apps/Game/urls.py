from django.urls import path
from . import views

app_name = "apps.Game"

urlpatterns = [
	path("solo/" , views.gamePage, name="solo-game-page") ,
	path("matchmaking/" , views.matchmakingPage, name="matchmaking-page")
]
