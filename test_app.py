#!/usr/bin/python3.7

import re
import sys

import pytest

import tornado.httpclient

import app

params = [("http://localhost:3000/api/v1/portal/1.4/1/", r'{"token": "[0-9][0-9][0-9][0-9]"}'),
          ("http://localhost:3000/api/v1/portal/1.4/2/", r'{"token": "[0-9][0-9][0-9][0-9]"}')]


def setup_module(module):
    pass


def teardown_module(module):
    pass


@pytest.fixture(scope="module")
def client():
    http_client = tornado.httpclient.HTTPClient()

    yield http_client

    http_client.close()


@pytest.mark.parametrize("path, rule", params)
def test_route(client, path, rule):
    try:
        response = client.fetch(path)
    except Exception as e:
        print("Error: %s" % e)
    else:
        assert re.match(rule, response.body.decode())
