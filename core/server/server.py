import sys

sys.path.append("./libs/tornado-routing")
import core.tokenizer.tokenizer

import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options

from core.tokenizer.tokenizer import app


class Server:
    def start(self, *args, **kwargs):
        pass

    def stop(self):
        pass

    def get_options(self):
        pass


class TornadoServer(Server):
    def __init__(self, params=None):
        super().__init__()

        self.__server = tornado.httpserver.HTTPServer(app.get_application())
        self.__loop = tornado.ioloop.IOLoop.instance()

        self.__options = tornado.options
        self.__options.define("port", default=3000,
                              help="Server listening port", type=int)
        self.__options.define(
            "address", default="192.168.12.10", help="Server listening address", type=str)

    def __del__(self):
        self.stop()

    def start(self):
        self.__server.listen(self.__options.options.port,
                             self.__options.options.address)
        try:
            # loop.add_callback(collectors[first_collector_id]._test)
            # loop.add_callback(collectors[first_collector_id]._destroy_all_srv)
            # loop.add_callback(collector.recv)
            # loop.call_later(1, collector._recv)
            # logging.debug("Max threads avalible: " + str(os.cpu_count()))
            self.__loop.start()
            logging.debug("Starting Web listen on: " +
                          self.__options.options.address + ':' + self.__options.options.port)
        except KeyboardInterrupt:
            logging.debug('Stopping')
            pass  # Press Ctrl+C to stop
        finally:
            self.stop()

    def stop(self):
        self.__loop.stop()

    def get_options(self):
        return self.__options
