from src.exceptions.invalid_message import InvalidMessage
from .message_handler import MessageHandler
from src.models.system_types import SystemTypes
from src.models.user import User
from src.models.message_types import MessageTypes
import re


class SystemHandler(MessageHandler):

    def __init__(self, client_handler):
        super().__init__(client_handler)

    def process_message(self, message):
        self.validate_message(message)
        if message.system_type == SystemTypes.NEW_USER:
            new_user = User(message.content)
            self.client_handler.user = new_user
            self.client_handler.handlers[new_user.name] = self.client_handler
            response = self.form_success_server_msg(content=f'User {new_user.name} entered chat',
                                                    message_type=MessageTypes.SYSTEM)
            self.client_handler.broadcast_message_to_everyone(response)
            self.client_handler.send_message(response)
        elif message.system_type == SystemTypes.EXIT:
            response = self.form_success_server_msg(content=f'User {self.client_handler.user.name} left chat',
                                                    message_type=MessageTypes.SYSTEM)
            self.client_handler.broadcast_message_to_everyone(response)
            self.client_handler.close()

    def validate_message(self, message):
        super().validate_message(message,
                                 ['system_type'],
                                 [('system_type', SystemTypes.list())])
        validators = {
            SystemTypes.NEW_USER: lambda: self.validate_new_user(message),
            SystemTypes.EXIT: self.validate_exit
        }
        validator = validators.get(message.system_type, None)
        if validator:
            validator()

    def validate_new_user(self, message):
        if not message.content:
            raise InvalidMessage('You need to pass a name inside of content')
        name_pattern = r'^[a-zA-Z]{4,12}$'
        if not re.match(name_pattern, message.content):
            raise InvalidMessage(
                'Name must include only alphabet symbols and length must be between 4 and 12'
            )
        if message.content == 'server' or message.content in self.client_handler.handlers:
            raise InvalidMessage(
                f'Name {message.content} already reserved! Please use another one'
            )

    def validate_exit(self):
        if not self.client_handler.user:
            raise InvalidMessage("You need to authenticate first")