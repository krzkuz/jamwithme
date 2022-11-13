import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from users.models import Profile
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from django.urls import reverse

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        conversation_id = text_data_json['conversationId'] 
        participants = text_data_json['participantsIdsList']

        # Find conversation
        conversation = await database_sync_to_async(Conversation.objects.get)(id=conversation_id)

        # Find message sender
        sender = await database_sync_to_async(Profile.objects.get)(user=self.scope['user'])
        user_id = str(sender.id)
        profile_picture = str(sender.image_url)
        link = reverse('profile', args=[user_id]) 
        
        
        if str(sender.id) in participants:
            if message != '':
                new_message = Message(
                    sender=sender,
                    body=message,
                    conversation=conversation,
                )
                await database_sync_to_async(new_message.save)()
                await database_sync_to_async(new_message.conversation.save)()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': user_id,
                    'profile_picture': profile_picture,
                    'link': link,
                    'conversation_id': conversation_id,
                }
            )


    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        profile_picture = event['profile_picture']
        link = event['link']
        if message != '':
            await self.send(text_data=json.dumps({
                'message': message,
                'user_id': user_id,
                'profile_picture': profile_picture,
                'link': link,
            }))
