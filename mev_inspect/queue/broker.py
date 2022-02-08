import os

from dramatiq.brokers.redis import RedisBroker


def connect_broker():
    return RedisBroker(host="redis-master", password=os.environ["REDIS_PASSWORD"])
