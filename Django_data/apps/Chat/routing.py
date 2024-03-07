from django.urls import path , include
from .consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    path("ws/chat" , ChatConsumer.as_asgi()) ,
]
