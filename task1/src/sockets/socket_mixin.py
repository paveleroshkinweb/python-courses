import socket
import logging
from contextlib import suppress
from exceptions.socket_closed import SocketIOError
from models.message import Message
from models.entity import Entity
from utils.decorators import check_if_socket_closed


@check_if_socket_closed(['send_message', 'receive_message', 'broadcast_message', 'send', '_recv_all'])
class SocketMixin:

    def __init__(self, sock, use_logging=True):
        self.socket = sock
        self.closed = False
        self.use_logging = use_logging

    def close(self):
        with suppress(Exception):
            self.socket.close()
            self.closed = True

    def send_message(self, message):
        packet_length, packet = message.to_bytes()
        self.send(packet_length, packet)

    def receive_message(self):
        message_length_bytes = self._recv_all(Entity.header_struct.size)
        message_length = Entity.header_struct.unpack(message_length_bytes)[0]
        message_bytes = self._recv_all(message_length)
        message = Message.from_bytes(message_bytes)
        self.log_info(f"Got a message {message} from {self.socket.getsockname()}")
        return message

    def broadcast_message(self, message, sockets):
        packet_length, packet = message.to_bytes()
        for sock in sockets:
            if self.socket.fileno() != sock.socket.fileno():
                with suppress(SocketIOError):
                    sock.send(packet_length, packet)

    def send(self, length_bytes, message_bytes):
        try:
            self.socket.send(length_bytes)
            self.socket.sendall(message_bytes)
            self.log_info(f"Sent a message {message_bytes.decode()} to {self.socket.getsockname()}")
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

    def log(self, level, text):
        if self.use_logging:
            getattr(logging, level)(text)

    def log_info(self, text):
        self.log('info', text)

    def log_error(self, text):
        self.log('error', text)
