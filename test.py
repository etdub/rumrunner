#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import random
import os

import zmq

from rumrunner import Rumrunner


class TestRumrunner(unittest.TestCase):

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
        from rumrunner import unmock_rumrunner, mock_rumrunner
        self.assertEqual(Rumrunner.MOCK, False)
        mock_rumrunner()
        self.assertEqual(Rumrunner.MOCK, True)
        unmock_rumrunner()
        self.assertEqual(Rumrunner.MOCK, False)


if __name__ == '__main__':
        unittest.main()
