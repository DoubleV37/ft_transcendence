from django.urls import path , include , re_path
from . import views

app_name = "apps.Game"

urlpatterns = [
	path("solo/" , views.gamePage, name="solo-game-page"),
 	path("parameters/", views.gameParameters, name="parameters"),
  path("modes/", views.modes, name="modes"),
  path("tournament/set/", views.tournament, name="tournament"),
  path("tournament/bracket/", views.bracket, name="bracket"),
	path("matchmaking/" , views.matchmakingPage, name="matchmaking-page"),
	path("<str:room_name>/" , views.multiGamePage, name="multiplayer-game-page")
]
