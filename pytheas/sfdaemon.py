import gevent
import logging
import time

from gevent.lock import Semaphore
from gevent.server import StreamServer

logging.basicConfig(filename="pytheas.log")
logger = logging.getLogger("pytheas")
logger.setLevel(logging.INFO)

class Pytheas(object):
    """
    Intended usage:
        Define your fetcher and sender classes (as extending from patterns.Fetcher
        and patterns.Sender). Then, create a Pytheas object from instances of
        those classes. Call the run method of this Pytheas object and you're set.
    """
    
    def __init__(self, fetcher, sender, sleep_time=1, command_interpreter=None, port=16981):
        """
        Instantiate a daemon object.

        fetcher -- A pytheas.patterns.Fetcher object.
        sender -- A pytheas.patters.Sender object.
        sleep_time -- Amount of sleep after every fetch/send iteration. Defaults
            to 1 second.
        port -- Port from which we listen for commands.
        """
        self.__fetcher = fetcher
        self.__sender = sender
        self.sleep_time = sleep_time
        if port:
            self.__external_server = StreamServer(("127.0.0.0", port), self.__listen_external)
        else:
            self.__external_server = None
        self.__ticket_counter = 1
        self.__ticket_counter_lock = Semaphore()

    def __sendfetch(self):
        self.__sender.send(self.__fetcher.fetch())
        gevent.sleep(1)

    def __listen_external(self, socket, address):
        """
        Sends two messages to any external client that has issued a command:
          - The first message is of the format "OK <ticketno>" where ticketno
            is a unique number identifying this transaction.
          - When it has finished processing the transaction and the processing
            is successful, it will send "T <ticketno>". Otherwise, send
            "F <ticketno>".

        All messages (commands and replies) are terminated by newlines (`\n`).
        """
        logger.info("external server received connection")
        sockfile = socket.makefile()

        while True:
            command = sockfile.readline()
            logger.info("issued command " + command)
            if not command:
                break
            else:
                ticketno = -1
                self.__ticket_counter_lock.acquire()
                ticketno = self.__ticket_counter
                self.__ticket_counter += 1
                self.__ticket_counter_lock.release()
                sockfile.write("OK " + str(ticketno))
                sockfile.write("T " + str(ticketno))
                sockfile.flush()

    def run(self):
        logger.info("Daemon started")

        if self.__external_server:
            self.__external_server.start()
            logger.info("External server started")
        
        while True:
            self.__sender.send(self.__fetcher.fetch())
            gevent.sleep(self.sleep_time)
