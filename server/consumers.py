import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.group_name = f"user_{self.scope['user'].id}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def power_update(self, event):
        await self.send(text_data=json.dumps(event))