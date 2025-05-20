import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebSocketConsumer
from chat.models import ChatMessage, ChatRoom
from user.models import User, OnlineUser
import asyncio

class ChatConsumer(AsyncWebSocketConsumer):
    def getuser(self, userId):
        return User.objects.get(id=userId)

    def get_online_users(self):
        all_users = OnlineUser.objects.all()
        users = [user.user.id for user in all_users]
        return users
    
    def add_online_user(self, user):
        try:
            OnlineUser.objects.create(user = user)
        except:
            pass

    def delete_online_user(self, user):
        try:
            OnlineUser.objects.get(user=user).delete()
        except:
            pass

    
    def savemessage(self, message, userId, roomId):
        user = User.objects.get(id=userId)
        room = ChatRoom.objects.get(id=roomId)
        chatemessage = ChatMessage.objects.create(
            user=user, 
            chat=room, 
            message=message
        )
        return {
            'action' : 'message',
            'user': userId,
            'room': roomId,
            'message':message,
            'userName':user.first_name,
            'timestamp':str(chatemessage.timestamp)

        }
    
    async def send_online_user_list(self):
        online_users = await database_sync_to_async(self.get_online_users)()
        chat_message = {
            'type': 'chat_message',
            'message': {
                'action': 'online_user',
                'online_users': online_users
            }
        }
    
    async def connect(self):
        #ver wrappers

        #dictionary containing metadata
        self.user_id = self.scope['url']['kwargs']['userId']
        #self.user = self.getuser(self.user_id) version asychronous
        self.user = await database_sync_to_async(self.getuser)(self.user_id)
        self.user_rooms = await database_sync_to_async(lambda: list(ChatRoom.objects.filter(member=self.user_id)))()

        await asyncio.gather(*[
            self.channel_layer.group_add(
                room.roomId, self.channel_name
            )
            for room in self.user_rooms
        ])
    
        await self.channel_layer.group_add('onlineUser', self.channel_name)

        await database_sync_to_async(self.addonlineuser)(self.user)

        await self.send_online_user_list()

        # accept websocket connection
        await self.accept()


    async def disconnect(self, close_code):
        await database_sync_to_async(self.delete_online_user)(self.user)
        await self.send_online_user_list()
        for room in self.user_rooms:
            await self.channel_layer.group_discard(
                room.roomId,
                self.channel_name
            )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        room_id = text_data_json['room']
        chatmessage = {}
        if action == 'message':
            message = text_data_json['message']
            user_id = text_data_json['user']
            chatmessage = await database_sync_to_async(self.savemessage)(message, user_id, room_id)
        
        await self.channel_layer.group_send(
            room_id, {
                'type': 'chat_message',
                'message': chatmessage
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))


        