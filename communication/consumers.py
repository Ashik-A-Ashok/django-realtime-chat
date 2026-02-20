# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.utils.timezone import now
# from accounts.models import User
# from .models import Message

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from accounts.models import User
from .models import Message


# ---------- SAFE DATABASE FUNCTIONS ----------

@database_sync_to_async
def set_user_online(user_id):
    User.objects.filter(id=user_id).update(is_online=True)

@database_sync_to_async
def set_user_offline(user_id):
    User.objects.filter(id=user_id).update(
        is_online=False,
        last_seen=now()
    )

@database_sync_to_async
def save_message(sender, receiver_id, message):
    receiver = User.objects.get(id=receiver_id)
    return Message.objects.create(
        sender=sender,
        receiver=receiver,
        content=message
    )


# ---------- PRESENCE CONSUMER ----------

class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        self.user = self.scope['user']
        self.group = 'online_users'

        await set_user_online(self.user.id)

        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            self.group,
            {
                'type': 'status',
                'user_id': self.user.id,
                'state': 'online'
            }
        )

    async def disconnect(self, close_code):
        await set_user_offline(self.user.id)

        await self.channel_layer.group_send(
            self.group,
            {
                'type': 'status',
                'user_id': self.user.id,
                'state': 'offline'
            }
        )

    async def status(self, event):
        await self.send(text_data=json.dumps(event))


# ---------- CHAT CONSUMER ----------

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        self.sender = self.scope['user']
        self.receiver_id = int(self.scope['url_route']['kwargs']['user_id'])

        self.room = f"chat_{min(self.sender.id, self.receiver_id)}_{max(self.sender.id, self.receiver_id)}"

        await self.channel_layer.group_add(self.room, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()

        if not message:
            return

        await save_message(self.sender, self.receiver_id, message)

        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'chat_message',
                'sender_id': self.sender.id,
                'sender': self.sender.username,
                'message': message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    


# ---------- PRESENCE ----------
# class PresenceConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         if not self.scope['user'].is_authenticated:
#             await self.close()
#             return

#         self.user = self.scope['user']
#         self.group = 'online_users'

#         User.objects.filter(id=self.user.id).update(is_online=True)

#         await self.channel_layer.group_add(self.group, self.channel_name)
#         await self.accept()

#         await self.channel_layer.group_send(
#             self.group,
#             {'type': 'status', 'user_id': self.user.id, 'state': 'online'}
#         )

#     async def disconnect(self, close_code):
#         User.objects.filter(id=self.user.id).update(
#             is_online=False,
#             last_seen=now()
#         )

#         await self.channel_layer.group_send(
#             self.group,
#             {'type': 'status', 'user_id': self.user.id, 'state': 'offline'}
#         )

#     async def status(self, event):
#         await self.send(text_data=json.dumps(event))


# ---------- CHAT ----------
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         if not self.scope['user'].is_authenticated:
#             await self.close()
#             return

#         self.sender = self.scope['user']
#         self.receiver_id = self.scope['url_route']['kwargs']['user_id']
#         self.room = f"chat_{min(self.sender.id,int(self.receiver_id))}_{max(self.sender.id,int(self.receiver_id))}"

#         await self.channel_layer.group_add(self.room, self.channel_name)
#         await self.accept()

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get('message')

#         if not message.strip():
#             return

#         receiver = User.objects.get(id=self.receiver_id)

#         Message.objects.create(
#             sender=self.sender,
#             receiver=receiver,
#             content=message
#         )

#         await self.channel_layer.group_send(
#             self.room,
#             {
#                 'type': 'chat_message',
#                 'sender': self.sender.username,
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps(event))
