import time
import ujson
import zmq

class Bootlegger(object):
  def __init__(self, metric_socket, app_name):
    self.metric_socket = metric_socket
    self.app_name = app_name

    self.context = zmq.Context()

    # Send metrics
    self.send_socket = self.context.socket(zmq.PUSH)
    self.send_socket.connect('ipc://{0}'.format(self.metric_socket))
    self.send_socket.setsockopt(zmq.LINGER, 0)

  def counter(self, metric_name, value=1):

    self.send_socket.send(ujson.dumps([self.app_name, metric_name, 'COUNTER',  value]))

  def gauge(self, metric_name, value):
    self.send_socket.send(ujson.dumps([self.app_name, metric_name, 'GAUGE', value]))

if __name__ == '__main__':
  m = Bootlegger('/var/tmp/metric_socket', 'test.app')
  for x in range(10):
    print x
    m.counter('test_counter', 1)
    m.gauge('test_gauge', x)
    time.sleep(1)
