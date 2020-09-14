import socket
import logging
from .tcp_socket import TCPSocket


class ServerSocket(TCPSocket):

    def __init__(self, config):
        super().__init__(config)
        self._configure()

    def _configure(self):
        try:
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.bind((self.config['address'], self.config['port']))
        except socket.error as e:
            self.exit_with_error(f"Can't bind to {self.config['address']}:{self.config['port']}, {e}")

    def start(self):
        self.listen(10)
        logging.info('')