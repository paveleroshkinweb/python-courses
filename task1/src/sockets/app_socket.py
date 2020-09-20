from .socket_mixin import SocketMixin
import socket
import sys
import logging


class AppSocket(SocketMixin):

    NO_FREE_PORTS_ERROR = 'No free ports available, please try later'
    BIND_ERROR = "Can't bind to {address}:{port}"
    CONNECTION_ERROR = "Can't connect to {s_address}:{s_port} from {address}:{port}"
    CONNECTION_SUCCESS = "Client {address}:{port} connected to {s_address}:{s_port}"
    LISTEN_ERROR = "Can't start server on {address}:{port}"
    LISTEN_SUCCESS = "Server listen {address}:{port}"
    UNKNOWN_PROBLEM = "Something went wrong, closing connection from {address}:{port} to {s_address}:{s_port}"

    def __init__(self, config, use_logging=True):
        super().__init__(socket.socket(socket.AF_INET, socket.SOCK_STREAM), use_logging)
        self.config = config
        self.bind()

    def bind(self):
        pass

    def exit(self, msg='', code=0):
        sys.stdout.flush()
        self.close()
        if msg:
            if code != 0:
                logging.error(msg)
            else:
                logging.info(msg)
        exit(code)

    def format(self, format_string, err=None):
        return format_string.format(**self.config) + (f'\n{err}' if err else '')
