import logging

import json

import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options
from tornado_routing import RoutingApplication, RequestRoutingHandler

from random import randint

define("port", default=3000, help="run on the given port", type=int)

logging.basicConfig(level=logging.DEBUG)
app = RoutingApplication()


class Tokenizer(RequestRoutingHandler):
    def __init__(self, *params):
        super().__init__(*params)
        self._load_data()
        self._changed = False

    def __del__(self):
        if (self._changed):
            with open("data.json", 'w') as file:
                self._items["__set_values"] = list(self._items["__set_values"])
                file.write(json.dumps(self._items))

    def _load_data(self):
        self._items = None

        try:
            with open("data.json") as file:
                self._items = json.load(file)
                self._items["__set_values"] = set(self._items["__set_values"])
        except Exception as e:
            self._items = {}
            self._items["__set_values"] = set()

    def _get_random_number(self):
        rand_number = -1

        while rand_number == -1:
            rand_number = randint(0, 9999)

            if rand_number in self._items["__set_values"]:
                rand_number = -1

        return rand_number

    def _get_token(self, path):
        new_attr = False
        child_items = self._items

        for i in path:
            if (new_attr):
                child_items[i] = {}
            elif (child_items.get(i) is None):
                child_items[i] = {}
                new_attr = True
                self._changed = True

            if (i != path[-1]):
                child_items = child_items[i]

        if (new_attr):
            rand_number = self._get_random_number()
            child_items[path[-1]] = str(rand_number).zfill(4)
            self._items["__set_values"].add(rand_number)

        return child_items[path[-1]]

    @app.route(r'/api/([^/]+)/([^/]+)/([^/]+)/([^/]+)/?', methods=['GET'])
    def get_token(self, *path):
        token = self._get_token(path)
        self.write({'token': token})


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app.get_application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
