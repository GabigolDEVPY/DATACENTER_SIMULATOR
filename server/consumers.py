import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UserStatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.group_name = f"user_{self.scope['user'].id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            await self.close(code=1011) # erro interno do servidor
        
             
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    # serviço é chamado quando existe updates dos dados do usuário
    async def power_update(self, event):
        await self.send(text_data=json.dumps(event))