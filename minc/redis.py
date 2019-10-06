import redis

r = redis.Redis(
        host='127.0.0.1',
        port=6379)


def check_thread(fcm, reg, post):
    if r.get((fcm, reg, post)):
        return False
    else:
        r.set((fcm, reg, post), True)
        return True
