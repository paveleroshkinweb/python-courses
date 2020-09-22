from .message_handler import MessageHandler
from exceptions.invalid_message import InvalidMessage


class TextHandler(MessageHandler):

    def __init__(self, client_handler):
        super().__init__(client_handler)

    def process_message(self, message):
        self.validate_message(message)
        self.client_handler.broadcast_message_to_everyone(
            self.form_success_msg(sender=self.client_handler.user.name, content=message.content)
        )

    def validate_message(self, message):
        super().validate_message(message, ['content'])
        if not self.client_handler.user:
            raise InvalidMessage("You need to authenticate first")