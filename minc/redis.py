import redis

r = redis.Redis(
        host='127.0.0.1',
        port=6379)


def check_thread(fcm, reg, post):
    key = '{}:{}:{}'.format(fcm, reg, post)
    if r.get(key):
        return False
    else:
        r.set(key, 'True')
        return True
