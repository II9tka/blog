import logging
import aioredis
import asyncio

from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer
from channels.exceptions import StopConsumer

from .services import (
    save_message, get_chat_or_raise_error, update_connection_status, get_messages, add_notification, get_notifications
)

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
        types: 'chat_message', 'chat_history', 'chat_leave', 'chat_join',
        actions: 'create_message', 'mark_message_as_read'
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room_name = ''
        self.room_group_name = ''

    async def _get_chat_or_raise_error(self):
        return await get_chat_or_raise_error(
            chat_id=self.room_name,
            user=self.user,
        )

    async def _update_connection_status(self, status):
        status_types = {
            'offline': 0,
            'online': 1
        }
        assert status_types.get(status, None), (
            'status "{status}" does not exist in status types.'.format(
                status=status
            )
        )
        await update_connection_status(
            user=self.user,
            status=status_types[status]
        )
        return status

    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            chat = await self._get_chat_or_raise_error()
            connection_status = await self._update_connection_status('online')

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
                    'action': 'connect',
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
            connection_status = await self._update_connection_status('offline')

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
        if action := content.get('type', None):
            if action == 'create_message':
                await self.create_message(content)
            elif action == 'mark_message_as_read':
                await self.mark_message_as_read(content)

    async def create_message(self, content):
        chat = await self._get_chat_or_raise_error()
        message = await save_message(
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
                'timestamp': message.timestamp.strftime("%m.%d.%Y, %H:%M"),
                "username": self.user.username,
                "message": content["message"],
            },
        )
        add_notification(
            message, user_id=self.user.id
        )
        logger.debug(
            'Notification successfully create in Redis. '
            'User notifications: {notifications}'.format(
                notifications=get_notifications(user_id=self.user.id)
            )
        )

    async def mark_message_as_read(self, content):
        pass

    async def get_last_messages(self):
        chat = await self._get_chat_or_raise_error()
        messages = await get_messages(chat)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_history",
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

    async def chat_history(self, event):
        await self.send_json(event)


# TODO: ChatNotifyConsumer Doesn't work. May be AsyncJsonWebsocketConsumer will help.

class ChatNotifyConsumer(AsyncHttpConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_streaming = False
        self.user = None

    async def handle(self, body):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            logger.info(
                'User "{username}" waiting for notifications.'.format(
                    username=self.user.username.title()
                )
            )
            await self.send_headers(headers=[
                (b"Cache-Control", b"no-cache"),
                (b"Content-Type", b"text/event-stream"),
                (b"Transfer-Encoding", b"chunked"),
            ])
            self.is_streaming = True
            asyncio.get_event_loop().create_task(self.stream())
        else:
            logger.info(
                'Trying to connect an unauthorized user'
            )
            raise StopConsumer('UNAUTHORIZED')

    async def disconnect(self):
        logger.info(
            'User "{username}" disconnected'.format(
                username=self.user.username.title(),
            ),
        )
        self.is_streaming = False

    async def stream(self):
        redis_connection = await aioredis.create_redis(settings.REDIS_URL)
        # ...
