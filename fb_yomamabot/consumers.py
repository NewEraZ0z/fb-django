# consumers.py

import json
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'user_{self.user_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']

        # Send message to Facebook Messenger
        self.send_message_to_facebook(sender_id, message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'from': 'agent'
        }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'from': 'user'
        }))

    def send_message_to_facebook(self, recipient_id, message):
        page_access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN  # Make sure you have this in your settings
        url = f"https://graph.facebook.com/v20.0/me/messages?access_token={page_access_token}"

        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")







# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
