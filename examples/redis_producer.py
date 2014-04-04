import pytheas.patterns
import pytheas.sfdaemon
import random
import string

import logging

from redis_patterns import RedisSender

logging.basicConfig(filename="pytheas.log")
logger = logging.getLogger("pytheas")
logger.setLevel(logging.INFO)


# Config stuff
PUT_LIST = "fetch_list"
REDIS_HOST = "localhost"
REDIS_PORT = 6379


class RandGenFetcher(pytheas.patterns.Fetcher):
    
    def fetch(self):
        return "".join([random.choice(string.lowercase) for i in range(5)])

if __name__ == "__main__":
    logger.info("Starting redis_producer")
    stringgen = RandGenFetcher()
    logger.info("Random fetcher instantiated")
    producer_sender = RedisSender(REDIS_HOST, REDIS_PORT, PUT_LIST)
    logger.info("Sender instantiated")
    producer_daemon = pytheas.sfdaemon.Pytheas(stringgen, producer_sender)
    logger.info("producer daemon instantiated")
    producer_daemon.run()
    logger.info("producer daemon started")
