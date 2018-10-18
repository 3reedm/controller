#!/usr/bin/python3.7
import re

import coverage
import tornado.testing

cov = coverage.Coverage()
cov.start()
import app
cov.stop()
cov.save()
cov.html_report()


class TestApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.app.get_application()

    def test_get(self):
        response = self.fetch('/api')
        self.assertEqual(
            response.body.decode(), "<html><title>{0}: {1}</title><body>{0}: {1}</body></html>".format("403", "Forbidden"))
        response = self.fetch('/app')
        self.assertEqual(
            response.body.decode(), "<html><title>{0}: {1}</title><body>{0}: {1}</body></html>".format("404", "Not Found"))
        response = self.fetch('/api/v1/portal/1.4/2')
        self.assertTrue(
            re.match(r'{"token": "[0-9]{4}"}', response.body.decode()))


all = TestApp


if __name__ == "__main__":
    tornado.testing.main()
