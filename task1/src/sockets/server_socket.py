import socket
from concurrent.futures import ThreadPoolExecutor
import logging
from .app_socket import AppSocket
from handlers.client_handler import ClientHandler


class ServerSocket(AppSocket):

    BACKLOG = 128
    MAX_CLIENTS = 2048

    def __init__(self, config):
        super().__init__(config, use_logging=True)
        self.handlers = {}

    def bind(self):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.config['address'], self.config['port']))
        except Exception as e:
            self.exit(self.format(self.BIND_ERROR, e), 1)

    def _listen(self):
        try:
            self.socket.listen(ServerSocket.BACKLOG)
            logging.info(self.LISTEN_SUCCESS.format(**self.config))
        except Exception as e:
            self.exit(self.format(self.LISTEN_ERROR, e), 1)

    def start(self):
        self._listen()
        with ThreadPoolExecutor(max_workers=ServerSocket.MAX_CLIENTS) as executor:
            while not self.closed:
                try:
                    client_socket, address = self.socket.accept()
                    logging.info(f'Client connected from {address[0]}:{address[1]}')
                    client_handler = ClientHandler(client_socket, self.handlers)
                    executor.submit(client_handler.handle)
                except socket.error as e:
                    self.exit(self.format(self.UNKNOWN_PROBLEM, e), 1)
