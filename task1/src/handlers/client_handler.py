import logging
from .handler import Handler
from .command_handler import CommandHandler
from .system_handler import SystemHandler
from .text_handler import TextHandler
from src.exceptions.invalid_message import InvalidMessage
from src.sockets.socket_mixin import SocketMixin
from src.models.message_types import MessageTypes


class ClientHandler(Handler, SocketMixin):

    def __init__(self, sock, handlers):
        Handler.__init__(self)
        SocketMixin.__init__(self, sock)
        self.message_handlers = {
            MessageTypes.TEXT: TextHandler(self),
            MessageTypes.COMMAND: CommandHandler(self),
            MessageTypes.SYSTEM: SystemHandler(self)
        }
        self.handlers = handlers
        self.active_game = None
        self.user = None

    def handle(self):
        logging.info(f'Handling the client from {self.socket.getsockname()}')
        try:
            while not self.closed:
                message = self.receive_message()
                self.process_message(message)
        except Exception as e:
            logging.error(e)
            if self.user:
                self.broadcast_message_to_everyone(
                    self.form_error_server_msg(content=f'Client {self.user.name} left unexpectedly'),
                )
        finally:
            self.close()
            if self.user.name in self.handlers:
                del self.handlers[self.user.name]

    def broadcast_message_to_everyone(self, message):
        SocketMixin.broadcast_message(self, message, self.handlers.values())

    def process_message(self, message):
        try:
            self.validate_message(message)
            handler = self.message_handlers[message.message_type]
            handler.process_message(message)
        except InvalidMessage as e:
            self.send_message(self.form_error_server_msg(content=str(e)))

    def validate_message(self, message):
        super().validate_message(message,
                                 ['message_type'],
                                 [('message_type', MessageTypes.list())])
