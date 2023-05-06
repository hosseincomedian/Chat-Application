import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .serializers import MessageSerializer, ChatRoomSerializer
from .models import Message, ChatRoom
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
import datetime
from time import sleep
from channels.db import database_sync_to_async
import asyncio

user = get_user_model()


class ChatRoomConsumer(AsyncWebsocketConsumer):



    async def new_message(self, data, mode='n'):
        message = await self.create_message_db(data, mode)
        result = await self.message_serializer(message)
        content = eval(result)
        await self.send_to_chat_message(content)

    async def left(self, message):

        await self.delete_chatroom_user_db()
        await self.new_message(message, 's')
        if await self.get_chatroom_user_count_db() == 0:
            await self.delete_chatroom_db()
        await self.disconnect(1001)

    async def fetch_message(self, message):

        qs = await self.get_chatroom_messages_db()
        message_json = await self.message_serializer(qs)

        content = {
            'message': eval(message_json),
            'command': 'fetch_message',
            'user': str(self.user.username)
        }
        await self.chat_message(content)

    async def message_serializer(self, query_set):
        morn = (lambda query_set: True if (
                query_set.__class__.__name__ == 'QuerySet') else False)(query_set)
        serialized = MessageSerializer(query_set, many=morn)
        data = await self.get_serilizer_data(serialized)
        content = (JSONRenderer().render(data))
        return content

    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        if self.room_name == 'all':
            self.page = 'home'
            self.user = self.scope["user"]
            async for room_group_name in await self.get_user_chatrooms_db():
                await (self.channel_layer.group_add)(
                    room_group_name.name,
                    self.channel_name
                )
        else:
            self.page = 'room'
            self.room_group_name = "chat_%s" % self.room_name
            try:
                self.chat_room = await self.get_chatroom_db()
            except:
                self.chat_room = await self.create_chatroom_db()
            num1 = await self.get_chatroom_user_count_db()
            await self.add_chatroom_user_db()
            num2 = await self.get_chatroom_user_count_db()

            await (self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            if num1 != num2:

                data = f'{self.user.username} joined the room'
                mode = 's'
                await self.new_message(data, mode)
        await self.accept()

    async def disconnect(self, close_code):
        if self.page == 'home':
            async for room_group_name in await self.get_user_chatrooms_db():
                await (self.channel_layer.group_discard)(
                    room_group_name.name,
                    self.channel_name,
                )
        else:
            await(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name,
            )

    async def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        message = text_data_dict.get('message', '')
        command = text_data_dict['command']
        if command == 'left':
            message = f'{self.user.username} left the room'
        await self.commands[command](self, message)


    async def fetch_for_home(self, message):
        qs = await self.sort_user_chatrooms_db()
        message_json = await self.chatroom_serializer(qs)

        content = {
            'message': eval(message_json),
            'command': 'fetch_for_update',
            'user': str(self.user.username)
        }
        return content

    async def send_to_chat_message(self, message):

        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                'command': 'new_message',
            }
        )

    async def chat_message(self, event):
        if self.page == 'home':
            event = await self.fetch_for_home('')
        await self.send(text_data=json.dumps(event))

    commands = {
        "new_message": new_message,
        "fetch_message": fetch_message,
        "left": left,
        "home": chat_message,
    }

    async def chatroom_serializer(self, query_set):

        serialized = ChatRoomSerializer(query_set, many=True)

        data = await self.get_serilizer_data(serialized)
        content = JSONRenderer().render(data)

        return content

    @database_sync_to_async
    def delete_chatroom_db(self):
        self.chat_room.delete()

    @database_sync_to_async
    def create_message_db(self, data, mode):
        return Message.objects.create(
            author=self.user, content=data, chatroom=self.chat_room, mode=mode)

    @database_sync_to_async
    def create_chatroom_db(self):
        return ChatRoom.objects.create(name=self.room_group_name)

    @database_sync_to_async
    def get_chatroom_db(self):
        return ChatRoom.objects.get(name=self.room_group_name)

    @database_sync_to_async
    def add_chatroom_user_db(self):
        self.chat_room.users.add(self.user)

    @database_sync_to_async
    def delete_chatroom_user_db(self):
        self.chat_room.users.remove(self.user)

    @database_sync_to_async
    def get_chatroom_user_count_db(self):
        return self.chat_room.users.count()

    @database_sync_to_async
    def get_chatroom_messages_db(self):
        return self.chat_room.mymessages(150)

    @database_sync_to_async
    def get_user_chatrooms_db(self):
        return self.user.chatrooms.all()

    @database_sync_to_async
    def get_serilizer_data(self, serialized):
        return serialized.data

    @database_sync_to_async
    def sort_user_chatrooms_db(self):
        qs = self.user.chatrooms.all()
        qs = (sorted(qs, key=lambda
            chatroom: chatroom.created_time if not chatroom.last_message else chatroom.last_message.timestamp,
                     reverse=True))
        return qs
