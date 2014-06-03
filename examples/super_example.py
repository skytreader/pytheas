import pytheas.patterns
import pytheas.sfdaemon
import gevent
import random
import redis
import string

import logging

logging.basicConfig(filename="pytheas.log")
logger = logging.getLogger("pytheas")
logger.setLevel(logging.INFO)


# Config stuff
PUT_LIST = "fetch_list"

FETCH_LIST = "fetch_list"
SEND_LIST = "send_list"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

logging.basicConfig(filename="pytheas.log")
logger = logging.getLogger("pytheas")
logger.setLevel(logging.INFO)

class RedisFetcher(pytheas.patterns.Fetcher):
    
    def __init__(self, redis_host, redis_port, fetch_list):
        self.__redis_connection = redis.StrictRedis(redis_host, redis_port)
        self.fetch_list = fetch_list
    
    def fetch(self):
        print "CONSUMER fetching"
        return self.__redis_connection.brpop(self.fetch_list)[1]

class RedisSender(pytheas.patterns.Sender):
    
    def __init__(self, redis_host, redis_port, send_list):
        self.__redis_connection = redis.StrictRedis(redis_host, redis_port)
        print "SENDER connection established"
        self.send_list = send_list

    def send(self, data):
        self.__redis_connection.lpush(self.send_list, data)
        print "SENDER Sent to redis: " + data


class RandGenFetcher(pytheas.patterns.Fetcher):
    
    def fetch(self):
        print "PRODUCER fetching"
        return "".join([random.choice(string.lowercase) for i in range(5)])

if __name__ == "__main__":
    print "Starting redis_producer"
    stringgen = RandGenFetcher()
    print "Random fetcher instantiated"
    producer_sender = RedisSender(REDIS_HOST, REDIS_PORT, PUT_LIST)
    print "Sender instantiated"
    producer_daemon = pytheas.sfdaemon.Pytheas(stringgen, producer_sender)
    print "producer daemon instantiated"
    
    local_fetcher = RedisFetcher(REDIS_HOST, REDIS_PORT, FETCH_LIST)
    local_sender = RedisSender(REDIS_HOST, REDIS_PORT, SEND_LIST)
    redis_daemon = pytheas.sfdaemon.Pytheas(local_fetcher, local_sender)

    hell = [gevent.spawn(producer_daemon.run), gevent.spawn(redis_daemon.run)]
    gevent.joinall(hell)
