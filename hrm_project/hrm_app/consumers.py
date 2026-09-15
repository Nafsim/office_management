from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import SupportConversation, SupportMessage


class SupportChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation = await self.get_conversation()
        if not self.user.is_authenticated or not self.conversation:
            await self.close(code=4403)
            return

        self.group_name = f'support_chat_{self.conversation_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        body = str(content.get('message', '')).strip()
        if not body:
            return
        message = await self.create_message(body)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'message': message,
        })

    async def chat_message(self, event):
        await self.send_json({'type': 'message', **event['message']})

    @database_sync_to_async
    def get_conversation(self):
        if not self.user.is_authenticated:
            return None
        conversation = SupportConversation.objects.filter(pk=self.conversation_id).first()
        if not conversation:
            return None
        if (
            self.user.id not in {conversation.requester_id, conversation.participant_id}
            and self.user.role not in ('manager', 'super_admin')
        ):
            return None
        return conversation

    @database_sync_to_async
    def create_message(self, body):
        message = SupportMessage.objects.create(
            conversation=self.conversation,
            sender=self.user,
            body=body,
        )
        return {
            'id': message.id,
            'message': message.body,
            'sender': self.user.get_full_name() or self.user.username,
            'sender_id': self.user.id,
            'created_at': message.created_at.isoformat(),
            'attachment_url': message.attachment.url if message.attachment else '',
            'attachment_name': message.attachment.name.rsplit('/', 1)[-1] if message.attachment else '',
        }