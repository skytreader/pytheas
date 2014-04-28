import gevent
import random

def task(pid):
    """
    Some non-deterministic task
    """
    total_sleep = 0
    print "Running " + str(pid)
    while True:
        r = random.randint(0, 2)
        total_sleep += r
        gevent.sleep(r*0.001)
        print "%s finished %s sleep" % (pid, r)
    print 'Task %s done with total sleep %s' % (pid, total_sleep)

def synchronous():
    for i in range(1,10):
        task(i)

def asynchronous():
    threads = [gevent.spawn(task, i) for i in xrange(10)]
    gevent.joinall(threads)

#print('Synchronous:')
#synchronous()

print('Asynchronous:')
asynchronous()
