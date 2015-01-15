#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import random
import os

import zmq

from rumrunner import Rumrunner


class TestRumrunner(unittest.TestCase):
    def test_send_counter_metric(self):
        ctx = zmq.Context()
        recv_socket = ctx.socket(zmq.PULL)
        tmp_metric_socket = '/var/tmp/test_metric_{0}'.format(random.random())
        recv_socket.bind('ipc://{0}'.format(tmp_metric_socket))

        Rumrunner(tmp_metric_socket, 'test_app').counter('test_counter')
        recv_socket.recv()  # suck out empty string for write test
        self.assertEqual(recv_socket.recv(),
                         '["test_app", "test_counter", "COUNTER", 1]')
        os.remove(tmp_metric_socket)

    def test_error_out_on_not_writable_socket_disable(self):
        ctx = zmq.Context()
        recv_socket = ctx.socket(zmq.PULL)
        tmp_metric_socket = '/var/tmp/test_metric_{0}'.format(random.random())
        recv_socket.bind('ipc://{0}'.format(tmp_metric_socket))

        Rumrunner(tmp_metric_socket, 'test_app', strict_check_socket=False)
        os.chmod(tmp_metric_socket, 0444)

        # Should not raise an exception due to permissions
        Rumrunner(tmp_metric_socket, 'test_app', strict_check_socket=False)
        os.remove(tmp_metric_socket)

    def test_error_out_on_not_writable_socket(self):
        ctx = zmq.Context()
        recv_socket = ctx.socket(zmq.PULL)
        tmp_metric_socket = '/var/tmp/test_metric_{0}'.format(random.random())
        recv_socket.bind('ipc://{0}'.format(tmp_metric_socket))

        Rumrunner(tmp_metric_socket, 'test_app')

        os.chmod(tmp_metric_socket, 0444)
        self.assertRaises(Exception, Rumrunner, tmp_metric_socket, 'test_app')
        os.remove(tmp_metric_socket)

    def test_mock_rumrunner(self):
        from rumrunner import unmock_rumrunner, mock_rumrunner, MockRumrunner
        self.assertTrue(isinstance(Rumrunner('/var/tmp/test', 'test_app',
                                             strict_check_socket=False),
                                   Rumrunner))
        mock_rumrunner()
        self.assertTrue(isinstance(Rumrunner('/var/tmp/test', 'test_app',
                                             strict_check_socket=False),
                                   MockRumrunner))
        unmock_rumrunner()
        self.assertTrue(isinstance(Rumrunner('/var/tmp/test', 'test_app',
                                             strict_check_socket=False),
                                   Rumrunner))


if __name__ == '__main__':
        unittest.main()
