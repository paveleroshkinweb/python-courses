import socket
import logging
import threading
import struct
import json
from exceptions.socket_closed import SocketIOError
from models.message import Message


class SocketHelper:

    header_struct = struct.Struct('!I')

    def __init__(self, sock):
        self.socket = sock
        self.closed = False
        self.lock = threading.RLock()

    def close(self):
        with self.lock:
            if not self.closed:
                try:
                    self.socket.close()
                    self.closed = True
                except socket.error as e:
                    logging.error(f"Couldn't close socket {self.socket.getsockname}\n{e}")

    def send_message(self, message):
        with self.lock:
            if self.closed:
                raise SocketIOError(f"Can't send message \n{message}\n due to closed socket")
            json_message = message.to_json()
            packet = json_message.encode()
            packet_length = SocketHelper.header_struct.pack(len(packet))
            try:
                self.socket.send(packet_length)
                self.socket.sendall(packet)
            except socket.error as e:
                raise SocketIOError(f"Can't send \n{message}\n, {e}")

    def receive_message(self):
        with self.lock:
            if self.closed:
                raise SocketIOError(f"Can't receive message due to closed socket")
            message_length_bytes = self._recv_all(SocketHelper.header_struct.size)
            message_length = SocketHelper.header_struct.unpack(message_length_bytes)[0]
            message_bytes = self._recv_all(message_length)
            message_json = message_bytes.decode()
            message = Message(**json.loads(message_json))
            return message

    def _recv_all(self, length):
        data = b''
        while len(data) < length:
            try:
                chunk = self.socket.recv(length)
            except socket.error as e:
                raise SocketIOError(f"Can't get message because of {e}")
            if not chunk:
                raise SocketIOError(
                    f'Socket {self.socket.getsockname()} closed with {length - len(data)} bytes left'
                )
            data += chunk
        return data
