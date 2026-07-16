from django.urls import path
from . consumers import ServerConsumer

websocket_urlpatterns = [
    path("ws/dashboard/", ServerConsumer.as_asgi()),
]
