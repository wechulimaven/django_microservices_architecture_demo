# import json
# from channels.generic.websocket import WebsocketConsumer

# class NotificationConsumer(WebsocketConsumer):
#     def connect(self):
#         self.user_id = self.scope['url_route']['kwargs']['user_id']
#         self.group_name = f'notifications_{self.user_id}'

#         # Join group based on user ID
#         self.accept()
#         self.channel_layer.group_add(self.group_name, self.channel_name)

#     def disconnect(self, close_code):
#         # Leave group
#         self.channel_layer.group_discard(self.group_name, self.channel_name)

#     def send_notification(self, event):
#         # Send message to WebSocket
#         self.send(text_data=json.dumps(event['message']))


import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"user_{self.user.id}"

        logger.info(f'User {self.user.id} connected')

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f'User {self.user.id} disconnected with code {close_code}')
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        logger.info(f'Received message: {message}')

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )

    async def send_notification(self, event):
        message = event['message']
        logger.info(f'Sending notification: {message}')

        await self.send(text_data=json.dumps({
            'message': message
        }))
