from django.urls import path
from . import views

app_name = "apps.Chat"

urlpatterns = [
	path("chat/" , views.chatPage, name="chat-page") ,
]
