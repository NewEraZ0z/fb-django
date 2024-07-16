# yomamabot/fb_yomamabot/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)
        # Handle incoming message here, e.g., save to database or process
        await self.send(text_data=json.dumps({
            'message': message
        }))
