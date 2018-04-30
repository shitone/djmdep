from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print('connect!')

    async def disconnect(self, close_code):
        await self.close()
        print('disconect!')

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['data']

        await self.send({
                "type": "websocket.send",
                "text": '2',
            })