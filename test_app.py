import re
import sys

import pytest

import tornado.httpclient

import app


# @pytest.mark.skipif(sys.version_info < (3, 5), reason="I don't want to run this test at the moment")
def test_route():
    paths = ["http://localhost:3000/api/v1/portal/1.4/1/",
             "http://localhost:3000/api/v1/portal/1.4/2/"]
    http_client = tornado.httpclient.HTTPClient()

    try:
        for path in paths:
            response = http_client.fetch(path)
    except Exception as e:
        print("Error: %s" % e)
    else:
        assert re.match(
            r'{"token": "[0-9][0-9][0-9][0-9]"}', response.body.decode())
