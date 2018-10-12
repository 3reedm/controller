#!/usr/bin/python3.7

import re
import sys

import unittest

import tornado.httpclient

import app


class TestApp(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.args = [("http://localhost:3000/api/v1/portal/1.4/1/", r'{"token": "[0-9][0-9][0-9][0-9]"}'),
                     ("http://localhost:3000/api/v1/portal/1.4/2/", r'{"token": "[0-9][0-9][0-9][0-9]"}')]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_route(self):
        for params in self.args:
            try:
                http_client = tornado.httpclient.HTTPClient()
                response = http_client.fetch(params[0])
            except Exception as e:
                print("Error: %s" % e)
            else:
                self.assertTrue(re.match(params[1], response.body.decode()))
            finally:
                http_client.close()


if __name__ == "__main__":
    unittest.main()
