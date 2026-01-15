import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, ConversationMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"conversation_{self.conversation_id}"

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Persist message to database
        saved_msg = await self.save_message(username, message)
        timestamp = saved_msg.created_at.strftime("%b %d, %Y %H:%M")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "timestamp": timestamp
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "timestamp": timestamp
        }))

    @database_sync_to_async
    def save_message(self, username, message):
        conversation = Conversation.objects.get(id=self.conversation_id)
        
        return ConversationMessage.objects.create(
            conversation=conversation,
            content=message,
            created_by=self.scope['user']
        )
