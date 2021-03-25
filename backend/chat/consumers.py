import logging

from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .services import save_message, get_chat_or_raise_error, update_connection_status, get_messages

User = get_user_model()

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    OFFLINE = 0
    ONLINE = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            chat = await get_chat_or_raise_error(
                chat_id=self.room_name,
                user=self.user,
            )
            connection_status = await update_connection_status(
                user=self.user,
                status=self.ONLINE
            )
            await self.channel_layer.group_add(
                chat.chat_name,
                self.channel_name,
            )
            logger.info(
                'User "{username}" connected'.format(
                    username=self.user.username.title()
                )
            )
            await self.accept()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_join",
                    "username": self.user.username,
                    'connection_status': connection_status
                },
            )
            await self.get_last_messages()
        else:
            logger.info(
                'Trying to connect an unauthorized user'
            )
            await self.close()

    async def disconnect(self, code):
        if self.user.is_authenticated:
            connection_status = await update_connection_status(
                user=self.user,
                status=self.OFFLINE
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_leave",
                    "username": self.user.username.title(),
                    'connection_status': connection_status
                },
            )
            logger.info(
                'User "{username}" closed chat'.format(
                    username=self.user.username.title()
                )
            )
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive_json(self, content, **kwargs):
        if content_type := content.get('type', None):
            if content_type == 'message':
                await self.message_handler(content)
            # elif content_type == '<...>':

    async def message_handler(self, content):
        chat = await get_chat_or_raise_error(
            chat_id=self.room_name,
            user=self.user,
        )
        await save_message(
            sender=self.user,
            chat=chat,
            text=content['message']
        )
        logger.info(
            'Message "{message_text}" from "{username}" has been successfully saved'.format(
                message_text=content['message'][:100],
                username=self.user.username.title()
            )
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "room": content['room'],
                "username": self.user.username,
                "message": content["message"],
            },
        )

    async def get_last_messages(self):
        chat = await get_chat_or_raise_error(
            chat_id=self.room_name,
            user=self.user,
        )
        messages = await get_messages(
            chat
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": self.user.username,
                'messages': messages
            },
        )

    async def chat_join(self, event):
        await self.send_json(event)

    async def chat_leave(self, event):
        await self.send_json(event)

    async def chat_message(self, event):
        await self.send_json(event)
