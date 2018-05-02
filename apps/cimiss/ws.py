from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print('connect!')

    async def disconnect(self, close_code):
        await self.close()
        print('disconect!')

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['data']

        await self.send_json(
            {"type": "websocket.send", "text": "2"}
        )
