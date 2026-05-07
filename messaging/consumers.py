import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        if not await self.user_in_conversation(user):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        user = self.scope["user"]

        msg_obj = await self.save_message(user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": msg_obj.content,
                "sender_id": user.id,
                "message_id": msg_obj.id,
            }
        )
        # after saving message
        msg = await self.save_message(user, message)

        # find recipient
        recipient_id = await self.get_other_user_id(user)

        # notify recipient inbox
        await self.channel_layer.group_send(
            f"user_{recipient_id}",
            {
            "type": "inbox.update"
            }
        )
        @database_sync_to_async
        def get_other_user_id(self, user):
        convo = Conversation.objects.get(id=self.conversation_id)

        return convo.participants.exclude(id=user.id).first().id

        async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

        @database_sync_to_async
        def user_in_conversation(self, user):
        return Conversation.objects.filter(
            id=self.conversation_id,
            participants=user
        ).exists()

        @database_sync_to_async
        def save_message(self, user, message):
        convo = Conversation.objects.get(id=self.conversation_id)

        return Message.objects.create(
            conversation=convo,
            sender=user,
            content=message
        )

class InboxConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        self.group_name = f"user_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def inbox_update(self, event):
        """
        This is triggered by backend when new message arrives
        """
        await self.send(text_data=json.dumps({
            "type": "inbox_update"
        }))
