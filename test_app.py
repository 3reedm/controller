#!/usr/bin/python3.7
import tornado.testing

import app


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
        self.assertEqual(
            response.body.decode(), '{"token": "0000"}')


all = TestApp


if __name__ == "__main__":
    tornado.testing.main()
