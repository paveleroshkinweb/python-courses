import socket
from concurrent.futures import ThreadPoolExecutor
import logging
from .app_socket import AppSocket
from .socket_helper import SocketHelper
from handlers.client_handler import ClientHandler


class ServerSocket(AppSocket):

    BIND_ERROR = "Can't bind to {address}:{port}"
    LISTEN_ERROR = "Can't start server on {address}:{port}"
    LISTEN_SUCCESS = "Server listen {address}:{port}"

    BACKLOG = 128
    MAX_CLIENTS = 2048

    def __init__(self, config):
        super().__init__(config)
        self.users = {}
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
            logging.info(ServerSocket.LISTEN_SUCCESS.format(**self.config))
        except socket.error as e:
            self.exit(ServerSocket.LISTEN_ERROR.format(**self.config) + f'\n{e}', 1)

    def start(self):
        self._listen()
        # handle exceptions !
        with ThreadPoolExecutor(max_workers=ServerSocket.MAX_CLIENTS) as executor:
            while True:
                client_socket, address = self.socket.accept()
                logging.info(f'Client connected from {address[0]}:{address[1]}')
                wrapped_socket = SocketHelper(client_socket)
                client_handler = ClientHandler(wrapped_socket, address, self)
                executor.submit(client_handler.handle)
