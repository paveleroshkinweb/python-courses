import socket
import logging
import threading
from contextlib import suppress
from exceptions.socket_closed import SocketIOError
from models.message import Message
from models.entity import Entity
from utils.lock import lock


@lock(['close', 'send_message', 'receive_message', 'broadcast_message', 'send'], threading.RLock)
class SocketHelper:

    def __init__(self, sock):
        self.socket = sock
        self.closed = False

    def close(self):
        try:
            self.socket.close()
            self.closed = True
        except socket.error as e:
            logging.error(f"Couldn't close socket {self.socket.getsockname}\n{e}")

    def send_message(self, message):
        packet_length, packet = message.to_bytes()
        self.send(packet_length, packet)

    def receive_message(self):
        message_length_bytes = self._recv_all(Entity.header_struct.size)
        message_length = Entity.header_struct.unpack(message_length_bytes)[0]
        message_bytes = self._recv_all(message_length)
        message = Message.from_bytes(message_bytes)
        return message

    def broadcast_message(self, message, sockets):
        packet_length, packet = message.to_bytes()
        for sock in sockets:
            if self.socket != sock:
                with suppress(SocketIOError):
                    sock.send(packet_length, packet)
                    yield message, sock  # ??? if I need it

    def send(self, length_bytes, message_bytes):
        try:
            self.socket.send(length_bytes)
            self.socket.sendall(message_bytes)
        except socket.error as e:
            raise SocketIOError(f"Can't send \n{message_bytes.decode()}\n, {e}")

    def _recv_all(self, length):
        data = b''
        while len(data) < length:
            chunk = self.socket.recv(length)
            if not chunk:
                raise SocketIOError(
                    f'Socket {self.socket.getsockname()} closed with {length - len(data)} bytes left'
                )
            data += chunk
        return data
