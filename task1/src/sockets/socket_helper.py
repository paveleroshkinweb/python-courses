from contextlib import suppress


class SocketHelper:

    chunk_size = 4096

    def __init__(self, sock):
        self.socket = sock
        self.closed = False

    def close(self):
        if not self.closed:
            with suppress(Exception):
                self.socket.close()
                self.closed = True

    def send_message(self, message):
        pass

    def recv_message(self):
        pass
