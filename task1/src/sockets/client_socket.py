import socket
import logging
from contextlib import suppress
import sys
from models.message import Message
import threading
from .app_socket import AppSocket


class ClientSocket(AppSocket):

    def __init__(self, config):
        super().__init__(config, use_logging=False)

    def bind(self):
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
                    self.exit(self.format(AppSocket.NO_FREE_PORTS_ERROR), 1)
        except Exception as e:
            self.exit(self.format(AppSocket.BIND_ERROR, e), 1)

    def _listen_messages(self):
        while not self.closed:
            try:
                message = self.receive_message()
                if message.content:
                    print_message = f'{message.from_whom} > {message.content}'
                    print(print_message)
            except socket.error:
                self.exit(self.format(AppSocket.UNKNOWN_PROBLEM), 1)

    def connect(self):
        try:
            self.socket.connect((self.config['s_address'], self.config['s_port']))
            logging.info(self.format(AppSocket.CONNECTION_SUCCESS))
        except Exception as e:
            self.exit(self.format(AppSocket.CONNECTION_ERROR, e), 1)

    def start_listen_messages(self):
        listen_thread = threading.Thread(target=self._listen_messages, daemon=True)
        listen_thread.start()

    def start(self):
        self.connect()
        self.start_listen_messages()
