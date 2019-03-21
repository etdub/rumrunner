import logging
import time


try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json
import zmq

logger = logging.getLogger(__name__)


class Rumrunner(object):
    MOCK = False

    def __init__(self, metric_socket, app_name, hwm=5000, block=False,
                 strict_check_socket=True):
        self.metric_socket = metric_socket
        self.app_name = app_name
        self.block = block

        self.context = zmq.Context()

        # Send metrics
        self.send_socket = self.context.socket(zmq.PUSH)
        self.send_socket.set_hwm(hwm)
        self.send_socket.connect('ipc://{0}'.format(self.metric_socket))
        self.send_socket.setsockopt(zmq.LINGER, 0)
        if strict_check_socket:
            self.test_socket_writable(strict_check_socket)

    def __new__(cls, *args, **kwargs):
        if cls.MOCK:
            return MockRumrunner(*args, **kwargs)
        else:
            return super(Rumrunner, cls).__new__(cls)

    def test_socket_writable(self, strict):
        if hasattr(zmq, 'COPY_THRESHOLD'):
            # Disable copy_threshold in order to allow copy=False, track=True
            # to work after pyzmq 17.0.0
            self.send_socket.copy_threshold = 0
        tracker = self.send_socket.send(''.encode('utf-8'), copy=False, track=True)
        try:
            tracker.wait(3)
        except zmq.NotDone:
            raise Exception('Metric socket not writable')
        if hasattr(zmq, 'COPY_THRESHOLD'):
            self.send_socket.copy_threshold = zmq.COPY_THRESHOLD

    def counter(self, metric_name, value=1):
        return self.send(metric_name, value, 'COUNTER')

    def gauge(self, metric_name, value):
        return self.send(metric_name, value, 'GAUGE')

    def percentile(self, metric_name, value):
        return self.send(metric_name, value, 'PERCENTILE')

    def send(self, metric_name, value, metric_type):
        try:
            datapoint = [self.app_name, metric_name, metric_type, value]
            if self.block:
                self.send_socket.send(json.dumps(datapoint).encode('utf-8'))
            else:
                self.send_socket.send(json.dumps(datapoint).encode('utf-8'), zmq.NOBLOCK)
            return True
        except zmq.error.Again as e:
            # Failed to send message
            logger.debug("Metric socket error - {0}".format(e))
            return False


class MockRumrunner(object):
    def __init__(self, *args, **kwargs):
        pass

    def counter(self, metric_name, value=1):
        pass

    def gauge(self, metric_name, value):
        pass

    def percentile(self, metric_name, value):
        pass

    def send(self, metric_name, value, metric_type):
        pass


def mock_rumrunner():
    Rumrunner.MOCK = True


def unmock_rumrunner():
    Rumrunner.MOCK = False

if __name__ == '__main__':
    m = Rumrunner('/var/tmp/metric_socket', 'test.app')
    s = time.time()
    for x in range(1000):
        if x % 100 == 0:
            print(x)
        m.counter('test_counter', 1)
        m.gauge('test_gauge', x)
        m.percentile('test_percentile.', x)
        time.sleep(0.000001)
    e = time.time()
    print("Took {0:.3f}s".format(e-s))
