from channels.middleware import BaseMiddleware
from django.db import close_old_connections

from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token

__all__ = ('TokenAuthMiddlewareStack',)


class TokenMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    scope['user'] = token.user
                    close_old_connections()
            except Token.DoesNotExist:
                pass
        return await self.inner(scope, receive, send)


def TokenAuthMiddlewareStack(inner):
    return TokenMiddleware(AuthMiddlewareStack(inner))
