import logging

from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware

from backend.chat.services import get_user_from_token

logger = logging.getLogger(__name__)

__all__ = ('TokenAuthMiddlewareStack',)


class TokenAuthMiddleware(BaseMiddleware):
    """Token authorization"""

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        auth_token = headers.get(b'sec-websocket-protocol', None)
        scope['user'] = await get_user_from_token(auth_token)
        return await self.inner(scope, receive, send)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
