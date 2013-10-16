import logging
import time
import ujson
import zmq

logger = logging.getLogger(__name__)

class Rumrunner(object):
    def __init__(self, metric_socket, app_name):
        self.metric_socket = metric_socket
        self.app_name = app_name

        self.context = zmq.Context()

        # Send metrics
        self.send_socket = self.context.socket(zmq.PUSH)
        self.send_socket.connect('ipc://{0}'.format(self.metric_socket))
        self.send_socket.setsockopt(zmq.LINGER, 0)

    def counter(self, metric_name, value=1):
        self.send(metric_name, value, 'COUNTER')

    def gauge(self, metric_name, value):
        self.send(metric_name, value, 'GAUGE')

    def percentile(self, metric_name, value):
        self.send(metric_name, value, 'PERCENTILE')

    def send(self, metric_name, value, metric_type):
        try:
            self.send_socket.send(ujson.dumps([self.app_name, metric_name, metric_type,  value]), zmq.NOBLOCK)
        except zmq.error.Again, e:
            logger.warn("Metric socket error - {0}".format(e))

if __name__ == '__main__':
    m = Rumrunner('/var/tmp/metric_socket', 'test.app')
    s = time.time()
    for x in range(1000):
        if x % 100 == 0:
            print x
        m.counter('test_counter', 1)
        m.gauge('test_gauge', x)
        m.percentile('test_percentile.', x)
        time.sleep(0.000001)
    e = time.time()
    print "Took {0:.3f}s".format(e-s)
