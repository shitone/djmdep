from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class MyConsumer(AsyncJsonWebsocketConsumer):
    def connect(self):
        self.room_group_name = 'aws'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print('connect!')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('disconect!')

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['data']

        self.send_json(
            {"type": "websocket.send", "text": "2"}
        )
