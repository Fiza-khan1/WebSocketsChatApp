# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            await self.accept()
            self.groupname = self.scope['url_route']['kwargs']['groupname']
            await self.channel_layer.group_add(self.groupname, self.channel_name)

            # Notify other users about the new user joining
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'user_status',
                    'username': self.scope['user'].username,
                    'status': 'online'
                }
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            # Notify other users about the user leaving
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'user_status',
                    'username': self.scope['user'].username,
                    'status': 'offline'
                }
            )
            await self.channel_layer.group_discard(self.groupname, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'message' in text_data_json:
            message = text_data_json['message']
            username = self.scope['user'].username

            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )
        elif 'typing' in text_data_json:
            typing = text_data_json['typing']
            username = self.scope['user'].username

            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'typing_status',
                    'typing': typing,
                    'username': username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def typing_status(self, event):
        typing = event['typing']
        username = event['username']
        await self.send(text_data=json.dumps({
            'typing': typing,
            'username': username
        }))

    async def user_status(self, event):
        username = event['username']
        status = event['status']
        await self.send(text_data=json.dumps({
            'user_status': {
                'username': username,
                'status': status
            }
        }))
