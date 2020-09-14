import socket
import logging
from contextlib import suppress


class TCPSocket(socket.socket):

    def __init__(self, config):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.config = config
        self.chunk_size = 4096

    def exit_with_error(self, msg='', code=1):
        with suppress(socket.error):
            super().close()
        if msg:
            logging.error(msg)
        exit(code)
