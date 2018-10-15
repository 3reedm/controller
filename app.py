#!/usr/bin/python3.7
import logging

from core.controller.controller import Controller
from core.server.server import TornadoServer
from core.client.client import Client

logging.basicConfig(level=logging.DEBUG)


def __main__():
    servers = [TornadoServer()]
    clients = [Client()]

    controller = Controller(servers[0], clients[0])


if __name__ == '__main__':
    __main__()
