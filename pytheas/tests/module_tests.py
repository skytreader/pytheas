import pytheas.patterns
import pytheas.sfdaemon

import gevent

import unittest

from gevent.queue import Queue

"""
Test plan description:

Create an in queue and an out queue. Preload the in queue with items. Create a
"daemon" that will fetch everything from the inqueue and put them in the out
queue. After n seconds (where n = the number of items in the queue), check if
everything in the in queue is removed and can now be found in the out queue.

Other plans:
    Record the internal state of the daemon. Distinguish between states where
    the last fetch returned something and where the last fetch returned none
    (i.e., read timed out). Instead of counting seconds, we can now just sleep
    until the daemon is returning the timed out status.
"""

in_queue = Queue()
out_queue = Queue()

class InQueueFetcher(pytheas.patterns.Fetcher):
    
    def fetch(self):
        print "Fetch"
        return in_queue.get()

class OutQueueSender(pytheas.patterns.Sender):
    
    def send(self, data):
        print "Send"
        out_queue.put_nowait(data)

class ModulesTest(unittest.TestCase):
    
    def setUp(self):
        fetcher = InQueueFetcher()
        sender = OutQueueSender()
        self.daemon = pytheas.sfdaemon.Pytheas(fetcher, sender)
        self.in_items = set(("houses", "jason mraz", "annie lennox", "vitamin string quartet"))

        for artist in self.in_items:
            in_queue.put(artist)

    def test_pytheas(self):
        wait_time = len(self.in_items)
        gevent.joinall([
        gevent.spawn(self.daemon.run),
        gevent.spawn(self.__actual_test)
        ])
        #gevent.sleep()

    def __actual_test(self):
        print "Running actual_test"
        self.assertEqual(in_queue.qsize(), 0)
        gevent.sleep()
 
if __name__ == "__main__":
    unittest.main()
