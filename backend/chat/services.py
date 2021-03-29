import logging
import json

from django.contrib.auth import get_user_model

from redis import StrictRedis

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer

from .models import Chat, Message
from .utils import get_redis
from ..account.models import AccountConnectionHistory

logger = logging.getLogger(__name__)

User = get_user_model()

__all__ = (
    'get_chat_or_raise_error',
    'save_message',
    'update_connection_status',
    'get_messages',
    'add_notification',
    'get_notifications',
)


# Django db

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
def update_connection_status(user, status, device_id: str = '1'):
    connection_history, _ = AccountConnectionHistory.objects.get_or_create(
        account=user, device_id=device_id
    )
    connection_history.connection_status = status
    connection_history.save(update_fields=['connection_status'])
    return status


@database_sync_to_async
def get_messages(chat):
    return [
        {
            'text': message.text,
            'timestamp': message.timestamp.strftime("%m.%d.%Y, %H:%M"),
            'sender': message.sender.username
        } for message in chat.messages.with_common_related().order_by('-timestamp')[:20]
    ]


# Redis db

def add_notification(message: Message, user_id: int = 1):
    r_strict = StrictRedis(**get_redis())
    r_strict.hset('%s_notifications' % user_id, message.id, json.dumps(
        {
            'id': message.id,
            'text': message.text,
            'timestamp': message.timestamp.strftime("%m.%d.%Y, %H:%M")
        }
    ))


def get_notifications(user_id):
    r_strict = StrictRedis(**get_redis())
    return r_strict.hgetall('%s_notifications' % user_id)


def read_notification(user_id, notification_id):
    r_strict = StrictRedis(**get_redis())
    data = json.loads(r_strict.hget('%s_notifications' % user_id, notification_id))
    data['read'] = True
