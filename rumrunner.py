import time
import ujson
import zmq

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

    try:
      self.send_socket.send(ujson.dumps([self.app_name, metric_name, 'COUNTER',  value]), zmq.NOBLOCK)
    except zmq.error.Again:
      pass

  def gauge(self, metric_name, value):
    try:
      self.send_socket.send(ujson.dumps([self.app_name, metric_name, 'GAUGE', value]), zmq.NOBLOCK)
    except zmq.error.Again:
      pass

if __name__ == '__main__':
  m = Rumrunner('/var/tmp/metric_socket', 'test.app')
  for x in range(1000):
    if x % 100 == 0:
      print x
    m.counter('test_counter', 1)
    m.gauge('test_gauge', x)
