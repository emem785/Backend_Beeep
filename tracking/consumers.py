import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import Beeep
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        phone = self.scope['url_route']['kwargs']['phone_number']
        self.room_name = phone
        self.room_group_name = 'chat_%s' % self.room_name
        beep_exists = await self.check_beep(phone)
        print(beep_exists)

        if beep_exists:
        # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        print(close_code)
        if close_code == 1006:
            pass
        else:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]
        lat = text_data_json['lat']
        lng = text_data_json['lng']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': type,
                'lat':lat,
                'lng':lng
            }
        )

    # Receive message from room group
    async def send_location(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
           'lat':event["lat"],
           'lng':event["lng"]
        }))

    async def stop_broadcast(self, event):
        await self.close()

    @database_sync_to_async
    def check_beep(self,phone):  
        try:      
            user = User.objects.get(username=phone)
            return Beeep.objects.filter(user=user,is_active=True).exists()
        except User.DoesNotExist:
            return False


