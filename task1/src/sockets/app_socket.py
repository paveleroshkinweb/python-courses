from .socket_helper import SocketHelper
import socket
import sys
import logging


class AppSocket(SocketHelper):

    def __init__(self, config, use_logging=True):
        super().__init__(socket.socket(socket.AF_INET, socket.SOCK_STREAM), use_logging)
        self.config = config

    def exit(self, msg='', code=0):
        sys.stdout.flush()
        self.close()
        if msg:
            if code != 0:
                logging.error(msg)
            else:
                logging.info(msg)
        exit(code)
