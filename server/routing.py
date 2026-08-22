from django.urls import path
from . consumers import UserStatsConsumer

websocket_urlpatterns = [
    path("ws/user-stats/", UserStatsConsumer.as_asgi()),
]
