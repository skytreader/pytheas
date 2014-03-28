import daemon
import time

class Pytheas(object):
    """
    Intended usage:
        Define your fetcher and sender classes (as extending from patterns.Fetcher
        and patterns.Sender). Then, create a Pytheas object from instances of
        those classes. Call the run method of this Pytheas object and you're set.
    """
    
    def __init__(self, fetcher, sender, sleep_time=1):
        self.__fetcher = fetcher
        self.__sender = sender
        self.sleep_time = sleep_time

    def run(self):
        with daemon.DaemonContext():
            while True:
                self.__sender.send(self.__fetcher.fetch())
                time.sleep(self.sleep_time)
