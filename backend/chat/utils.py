from django.conf import settings


def get_redis():
    return {
        'host': getattr(settings, 'REDIS_HOST', '127.0.0.1'),
        'port': getattr(settings, 'REDIS_PORT', 6379)
    }
