from django.urls import path
from . import views

app_name = "apps.Game"

urlpatterns = [
	path("room/" , views.gamePage, name="room-page") ,
]
