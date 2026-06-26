from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        self.group_name = "chat_global"

        from asgiref.sync import async_to_sync 
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event["message"]))