import pytheas.patterns
import pytheas.sfdaemon
import random
import string

from redis_patterns import RedisSender


# Config stuff
PUT_LIST = "fetch_list"
REDIS_HOST = "localhost"
REDIS_PORT = 6379


class RandGenFetcher(pytheas.patterns.Fetcher):
    
    def fetch(self):
        return "".join([random.choice(string.lowercase) for i in range(5)])

stringgen = RandGenFetcher()
producer_sender = RedisSender(REDIS_HOST, REDIS_PORT, PUT_LIST)
producer_daemon = pytheas.sfdaemon.Pytheas(stringgen, producer_sender)
producer_daemon.run()
