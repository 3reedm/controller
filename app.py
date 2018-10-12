#!/usr/bin/python3.7

import logging
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.options

sys.path.append("./tornado-routing")
import tokenizer.tokenizer

from random import randint

from tornado.options import define, options

from tokenizer.tokenizer import app


define("port", default=3000, help="run on the given port", type=int)

logging.basicConfig(level=logging.DEBUG)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app.get_application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
