import socket


class SocketIOError(socket.error):
    """ Socket already closed error for I/O related errors """
