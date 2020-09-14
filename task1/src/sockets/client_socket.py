import socket
import logging
from contextlib import suppress
from .app_socket import AppSocket


class ClientSocket(AppSocket):

    NO_FREE_PORTS_ERROR = 'No free ports available, please try later'
    BIND_ERROR = "Can't bind to {address}"
    CONNECTION_ERROR = "Can't connect to {s_address}:{s_port} from {address}:{port}"

    def __init__(self, config):
        super().__init__(config)
        self._configure()

    def _configure(self):
        try:
            if self.config['port']:
                self.socket.bind((self.config['address'], self.config['port']))
            else:
                for port in range(1025, 65536):
                    with suppress(socket.error):
                        self.socket.bind((self.config['address'], port))
                        self.config['port'] = port
                        break
                else:
                    self.exit(ClientSocket.NO_FREE_PORTS, 1)
        except socket.error as e:
            self.exit(ClientSocket.BIND_ERROR.format(**self.config) + f'\n{e}', 1)

    def _connect(self):
        try:
            self.socket.connect((self.config['s_address'], self.config['s_port']))
        except socket.error as e:
            self.exit(ClientSocket.CONNECTION_ERROR.format(**self.config) + f'\n{e}', 1)

    def start(self):
        self._connect()