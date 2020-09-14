import socket
import threading
import logging
from .app_socket import AppSocket


class ServerSocket(AppSocket):

    BIND_ERROR = "Can't bind to {address}:{port}"
    LISTEN_ERROR = "Can't start server on {address}:{port}"

    BACKLOG = 128
    MAX_CLIENTS = 1024

    def __init__(self, config):
        super().__init__(config)
        self._configure()

    def _configure(self):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.config['address'], self.config['port']))
        except socket.error as e:
            self.exit(ServerSocket.BIND_ERROR.format(**self.config) + f'\n{e}', 1)

    def _listen(self):
        try:
            self.socket.listen(ServerSocket.BACKLOG)
            logging.info(f"Server listen {self.config['address']}:{self.config['port']}")
        except socket.error as e:
            self.exit(ServerSocket.LISTEN_ERROR.format(**self.config) + f'\n{e}', 1)

    def start(self):
        self._listen()
        while True:
            client_socket, address = self.socket.accept()
            print(address)

