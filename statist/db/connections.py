import redis
import os


REDIS_USERNAME = os.environ.get('REDIS_USERNAME', None)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)



def get_redis_connection(host, port, username=REDIS_USERNAME, password=REDIS_PASSWORD):
    client_kwargs = {
        'host': host,
        'port': port,
        'decode_responses': True
    }
    if REDIS_PASSWORD:
        client_kwargs['password'] = REDIS_PASSWORD
    if REDIS_USERNAME:
        client_kwargs['username'] = REDIS_USERNAME

    return redis.Redis(**client_kwargs)
