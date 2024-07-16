# # yomamabot/fb_yomamabot/consumers.py

# fb_yomamabot/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "chat_room"
        self.room_group_name = "chat_%s" % self.room_name

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))




# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
    
#     def disconnect(self, close_code):
#         pass
    
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Broadcast the message to the group
#         async_to_sync(self.channel_layer.group_send)(
#             'chat_group',
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     def chat_message(self, event):
#         message = event['message']
        
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))








# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         message = json.loads(text_data)
#         # Handle incoming message here, e.g., save to database or process
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
