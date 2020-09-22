from .handler import Handler


class MessageHandler(Handler):

    def __init__(self, client_handler):
        super().__init__()
        self.client_handler = client_handler

    def process_message(self, message):
        raise NotImplementedError("Subclass must implement abstract method")
