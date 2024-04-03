from django.urls import path
from . import views

app_name = "apps.Game"

urlpatterns = [
	path("room/" , views.gamePage, name="room-page"),
 	path("parameters/", views.gameParameters, name="parameters"),
  	path("modes/", views.modes, name="modes"),
    path("tournament/", views.tournament, name="tournament"),
]
