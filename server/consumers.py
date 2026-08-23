import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import UserService
from channels.db import database_sync_to_async

class ServerConsumer(AsyncWebsocketConsumer):
    def connect(self):
        pass