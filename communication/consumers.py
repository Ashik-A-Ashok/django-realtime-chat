import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from django.apps import apps


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.user = self.scope["user"]
        self.group_name = "online_users"

        await self.set_online(self.user.id)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "status",
                "user_id": self.user.id,
                "state": "online",
            },
        )

    async def disconnect(self, close_code):
        await self.set_offline(self.user.id)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "status",
                "user_id": self.user.id,
                "state": "offline",
            },
        )

    async def status(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def set_online(self, user_id):
        User = apps.get_model("accounts", "User")
        User.objects.filter(id=user_id).update(is_online=True)

    @database_sync_to_async
    def set_offline(self, user_id):
        User = apps.get_model("accounts", "User")
        User.objects.filter(id=user_id).update(
            is_online=False,
            last_seen=now(),
        )


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.sender = self.scope["user"]
        self.receiver_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        self.room_name = f"chat_{min(self.sender.id, self.receiver_id)}_{max(self.sender.id, self.receiver_id)}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        await self.save_message(self.sender.id, self.receiver_id, message)

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "sender_id": self.sender.id,
                "message": message,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        Message = apps.get_model("communication", "Message")
        return Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=message,
        )