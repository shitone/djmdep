from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class AWSPQCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'aws_info'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send2client(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(
            {
                'message': message
            }
        ))

