import time
import ujson
import zmq

class Smuggler(object):
  def __init__(self, metric_socket, app_name):
    self.metric_socket = metric_socket
    self.app_name = app_name

    self.context = zmq.Context()

    # Send metrics
    self.send_socket = self.context.socket(zmq.PUSH)
    self.send_socket.connect('ipc://{0}'.format(self.metric_socket))

  def counter(self, metric_name, value=1):

    self.send_socket.send(ujson.dumps([self.app_name, metric_name, 'COUNTER',  value]))

  def gauge(self, metric_name, value):
    self.send_socket.send(ujson.dumps([self.app_name, metric_name, 'GAUGE', value]))

if __name__ == '__main__':
  m = Smuggler('/var/tmp/metric_socket', 'test.app')
  for x in range(10):
    m.counter('test_counter', 1)
    time.sleep(1)
