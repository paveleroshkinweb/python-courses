import socket
from src.models.user import User
from src.models.message import Message
from src.models.message_types import MessageTypes
from src.models.system_types import SystemTypes
from src.models.commands import Commands
import re


class ClientHelper:

    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.user = None

    def recv_and_show_new_message(self):
        message = self.client_socket.receive_message()
        if message.content:
            print_message = f'{message.sender} > {message.content}'
            print(print_message)
        return message

    def listen_messages(self):
        try:
            while not self.client_socket.closed:
                self.recv_and_show_new_message()
        except socket.error as e:
            self.client_socket.exit(
                self.client_socket.format(self.client_socket.UNKNOWN_PROBLEM, e), 1
            )

    def set_user(self):
        try:
            name = input('Username: ').strip()
            message = self._new_user_message(name)
            self.client_socket.send_message(message)
            response = self.recv_and_show_new_message()
            if not response.success:
                self.set_user()
            else:
                self.user = User(message.content)
        except socket.error as e:
            self.client_socket.exit(
                self.client_socket.format(self.client_socket.UNKNOWN_PROBLEM, e), 1
            )

    def listen_client_messages(self):
        try:
            while not self.client_socket.closed:
                text = input().strip()
                try:
                    message = self.parse_text(text)
                    self.client_socket.send_message(message)
                    if message.system_type == SystemTypes.EXIT:
                        self.client_socket.exit('Disconnecting from server...')
                except ValueError as e:
                    print(e)
        except socket.error as e:
            self.client_socket.exit(
                self.client_socket.format(self.client_socket.UNKNOWN_PROBLEM, e), 1
            )

    def _new_user_message(self, name):
        return Message(**{
            'message_type': MessageTypes.SYSTEM,
            'content': name,
            'system_type': SystemTypes.NEW_USER,
        })

    def _exit_message(self):
        return Message(**{
            'message_type': MessageTypes.SYSTEM,
            'system_type': SystemTypes.EXIT
        })

    def _command_message(self, command, **kwargs):
        return Message(**{
            'message_type': MessageTypes.COMMAND,
            'command': command,
            **kwargs
        })

    def _text_message(self, content):
        return Message(**{
            'message_type': MessageTypes.TEXT,
            'content': content
        })

    def _process_game_step(self, regex, text):
        content = re.match(regex, text).group(1).strip()
        return self._command_message(Commands.GAME_STEP, content=content)

    def _process_private_message(self, regex, text):
        res = re.match(regex, text)
        selected_users = [user for user in res.group(1).strip().split(' ') if user != '']
        content = res.group(2).strip()
        if not selected_users or not content:
            raise ValueError("Users to send and message can't be empty!")
        return self._command_message(Commands.PRIVATE_MESSAGE,
                                     selected_users=selected_users,
                                     content=content)

    def _process_server_time_message(self):
        return Message(message_type=MessageTypes.COMMAND, command=Commands.SERVER_TIME)

    def parse_text(self, text):
        processors = [
            (r'^!EXIT!$', lambda _: self._exit_message()),
            (r'^cmd!%s$' % Commands.PARTICIPANTS_COUNT, lambda _: self._command_message(Commands.PARTICIPANTS_COUNT)),
            (r'^cmd!%s$' % Commands.PARTICIPANTS, lambda _: self._command_message(Commands.PARTICIPANTS)),
            (r'^cmd!%s$' % Commands.ROCK_PAPER_SCISSORS, lambda _: self._command_message(Commands.ROCK_PAPER_SCISSORS)),
            (r'^cmd!%s:(.+)$' % Commands.GAME_STEP, lambda regex: self._process_game_step(regex, text)),
            (r'^cmd!%s(.+):(.+)$' % Commands.PRIVATE_MESSAGE, lambda regex: self._process_private_message(regex, text)),
            (r'^cmd!%s$' % Commands.SERVER_TIME, lambda _: self._process_server_time_message()),
            (r'.+', lambda _: self._text_message(text))
        ]
        for pattern, command in processors:
            if re.match(pattern, text):
                return command(pattern)
        raise ValueError('Empty messages are not allowed!')
