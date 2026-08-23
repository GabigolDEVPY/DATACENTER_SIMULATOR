from django.urls import path
from .consumers import ServerConsumer

websocket_urlpatterns = [
    path("ws/server", ServerConsumer.as_asgi(), name="server_websocket")
]