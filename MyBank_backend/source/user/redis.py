import redis
from django.conf import settings

redis_cli = redis.Redis(
            host=settings.REDIS_SETTINGS['host'],
            port=settings.REDIS_SETTINGS['port'],
            db=settings.REDIS_SETTINGS['db']
        )