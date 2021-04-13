import logging
import json
import aioredis
from django.conf import settings

from rest_framework.authtoken.models import Token

from django import db
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from redis import StrictRedis

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer

from .models import Chat, Message
from .utils import get_redis
from ..account.models import AccountConnectionHistory

logger = logging.getLogger(__name__)

User = get_user_model()
REDIS_URL = settings.REDIS_URL

__all__ = (
    'get_chat_or_raise_error',
    'save_message',
    'update_connection_status',
    'get_last_messages',
    'add_notification',
    'get_notifications',
    'get_user_from_token',
)


# Django db

@database_sync_to_async
def get_user_from_token(auth_header):
    try:
        _, token = auth_header.decode().split()
    except (ValueError, AttributeError):
        token = ''
    try:
        token = Token.objects.select_related('user').get(key=token)
        user = token.user
    except Token.DoesNotExist:
        user = AnonymousUser()

    db.close_old_connections()
    return user


@database_sync_to_async
def get_chat_or_raise_error(chat_id, user):
    if not user.is_authenticated:
        logger.warning(
            'Trying to connect to chat "{chat_id}" an unauthorized user'.format(
                chat_id=chat_id,
            )
        )
        raise StopConsumer('USER_UNAUTHORIZED')
    try:
        room = Chat.objects.get(id=chat_id)
    except (Chat.DoesNotExist, ValueError):
        logger.error(
            'User "{username}" attempt to move to a non-existent chat {chat_id}'.format(
                username=user.username.title(),
                chat_id=chat_id
            )
        )
        raise StopConsumer('CHAT_ROOM_DOES_NOT_EXIST')
    return room


@database_sync_to_async
def save_message(**kwargs):
    return Message.objects.create(
        **kwargs
    )


@database_sync_to_async
def update_connection_status(user: User, status: int, session_id: str):
    connection_history, _ = AccountConnectionHistory.objects.get_or_create(
        account=user, session_id=session_id
    )
    connection_history.connection_status = status
    connection_history.save(update_fields=['connection_status'])
    return status


@database_sync_to_async
def get_last_messages(chat):
    return [
        {
            'id': message.id,
            'text': message.text,
            'timestamp': message.timestamp.strftime("%m.%d.%Y, %H:%M"),
            'sender': message.sender.username
        } for message in chat.messages.all().order_by('-timestamp')[:20]
    ]


# Redis db


def add_notification(message: Message, user_id: int = 1):
    r_strict = StrictRedis(**get_redis())
    r_strict.hset('notifications_%s:chat_%s' % (user_id, message.chat.id), message.id, json.dumps(
        {
            'id': message.id,
            'text': message.text,
            'timestamp': message.timestamp.strftime("%m.%d.%Y, %H:%M")
        }
    ))
    # r_strict.publish('%s_notifications_%s_chat' % (user_id, message.chat.id), json.dumps(
    #     {
    #         'id': message.id,
    #         'text': message.text,
    #         'timestamp': message.timestamp.strftime("%m.%d.%Y, %H:%M")
    #     }
    # ))


def get_notifications(user_id):
    r_strict = StrictRedis(**get_redis())
    return r_strict.hgetall('%s_notifications' % user_id)
