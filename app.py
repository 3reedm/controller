#!/usr/bin/python3.7
import logging

import sys

sys.path.insert(1, "./ex-libs/tornado-routing")
import core.tokenizer.tokenizer

import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options

from core.tokenizer.tokenizer import app

define("port", default=3000,
       help="Server listening port", type=int)
define("address", default="192.168.12.10",
       help="Server listening address", type=str)

logging.basicConfig(filename="server.log", level=logging.DEBUG)


def __main__():
    server = tornado.httpserver.HTTPServer(app.get_application())
    io_loop = tornado.ioloop.IOLoop.instance()
    options = tornado.options.options

    server.listen(options.port, options.address)
    try:
        logging.debug("Starting Web listen on: " +
                      options.address + ':' + str(options.port))
        io_loop.start()
    except KeyboardInterrupt:
        logging.debug('Stopping\n')
        pass  # Press Ctrl+C to stop
    finally:
        io_loop.stop()


if __name__ == '__main__':
    __main__()
