import socket
from sockets.app_socket import AppSocket
from models.user import User


class ClientHelper:



    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.user = None

    def recv_and_show_new_message(self):
        message = self.client_socket.receive_message()
        if message.content:
            print_message = f'{message.from_whom} > {message.content}'
            print(print_message)
        return message

    def listen_messages(self):
        try:
            while not self.client_socket.closed:
                self.recv_and_show_new_message()
        except socket.error:
            self.client_socket.exit(self.client_socket.format(AppSocket.UNKNOWN_PROBLEM), 1)

    def set_user(self):
        try:
            text = input('Username: ')
            message = ClientHelper.parse_text(text)
            self.client_socket.send_message(message)
            response = self.recv_and_show_new_message()
            if not response.success:
                self.set_user()
            else:
                self.user = User(message.content)
        except socket.error:
            self.client_socket.exit(self.client_socket.format(AppSocket.UNKNOWN_PROBLEM), 1)

    def listen_client_messages(self):
        try:
            while not self.client_socket.closed:
                text = input(f'{self.user} > ')
                # TO DO
        except socket.error:
            self.client_socket.exit(self.client_socket.format(AppSocket.UNKNOWN_PROBLEM), 1)

    @staticmethod
    def parse_text(text):
        pass