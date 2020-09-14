import socket
from contextlib import suppress
from .tcp_socket import TCPSocket


class ClientSocket(TCPSocket):

    def __init__(self, config):
        super().__init__(config)
        self._configure()

    def _configure(self):
        try:
            if self.config['port']:
                self.bind((self.config['address'], self.config['port']))
            else:
                for port in range(1025, 65535):
                    with suppress(socket.error):
                        self.bind((self.config['address'], port))
                        self.config['port'] = port
                        break
                else:
                    self.exit_with_error('No free ports available, please try later')
        except Exception as e:
            self.exit_with_error(f"Can't bind to {self.config['address']}, {e}")

    def start(self):
        pass