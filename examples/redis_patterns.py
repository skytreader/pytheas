import pytheas.patterns
import pytheas.sfdaemon
import redis
import logging

# Config stuff
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
        return self.__redis_connection.brpop(self.fetch_list)[1]

class RedisSender(pytheas.patterns.Sender):
    
    def __init__(self, redis_host, redis_port, send_list):
        self.__redis_connection = redis.StrictRedis(redis_host, redis_port)
        #logger.info("RedisSender connection established")
        self.send_list = send_list

    def send(self, data):
        self.__redis_connection.lpush(self.send_list, data)
        #logger.info("Sent to redis: " + data)

if __name__ == "__main__":
    local_fetcher = RedisFetcher(REDIS_HOST, REDIS_PORT, FETCH_LIST)
    local_sender = RedisSender(REDIS_HOST, REDIS_PORT, SEND_LIST)
    redis_daemon = pytheas.sfdaemon.Pytheas(local_fetcher, local_sender)
    redis_daemon.run()
