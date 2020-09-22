import socket
import logging
from contextlib import suppress

import threading
from .app_socket import AppSocket
from src.helpers.client_helper import ClientHelper


class ClientSocket(AppSocket):

    def __init__(self, config):
        super().__init__(config, use_logging=False)
        self.client_helper = ClientHelper(self)

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
                    self.exit(self.format(self.NO_FREE_PORTS_ERROR), 1)
        except Exception as e:
            self.exit(self.format(self.BIND_ERROR, e), 1)

    def connect(self):
        try:
            self.socket.connect((self.config['s_address'], self.config['s_port']))
            logging.info(self.format(self.CONNECTION_SUCCESS))
        except Exception as e:
            self.exit(self.format(self.CONNECTION_ERROR, e), 1)

    def start_listen_server_messages(self):
        listen_thread = threading.Thread(target=self.client_helper.listen_messages,
                                         daemon=True,
                                         name='listen_messages')
        listen_thread.start()

    def start(self):
        self.connect()
        self.client_helper.set_user()
        self.start_listen_server_messages()
        self.client_helper.listen_client_messages()
