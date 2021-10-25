import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import ChatRoom, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        target_username = self.scope['url_route']['kwargs']['username']
        user = self.scope['user']
        chat_room = await self.get_chat_room(user, target_username)
        chat_room_channel = f'chat_room_{chat_room.id}'

        self.chat_room = chat_room
        self.chat_room_name = chat_room_channel
        await self.channel_layer.group_add(self.chat_room_name, self.channel_name)

        await self.send(dict(type='websocket.accept'))

    async def websocket_receive(self, event):
        text = event.get('text', '{}')

        data = json.loads(text)
        message_text = data.get('message')
        if not message_text:
            return
        await self.create_chat_message(message_text)

        response_data = dict(message=message_text, username=self.scope['user'].username)
        new_event = dict(type='chat_message', text=json.dumps(response_data))

        await self.channel_layer.group_send(self.chat_room_name, new_event)

    async def chat_message(self, event):
        response_text = event.get('text', None)
        # Send message to WebSocket
        await self.send(dict(type='websocket.send', text=response_text))

    @database_sync_to_async
    def get_chat_room(self, user, target_username):
        user_class = get_user_model()
        target_user = user_class.objects.get(username=target_username)
        return ChatRoom.objects.get_or_create(user, target_user)[0]

    @database_sync_to_async
    def create_chat_message(self, message):
        chat_message = ChatMessage(chat_room=self.chat_room, user=self.scope['user'], message=message)
        chat_message.save()
