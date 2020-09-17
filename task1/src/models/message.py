from .entity import Entity


class Message(Entity):

    def __init__(self, message_type, timestamp, content, from_whom, to_whom=None, command=None):
        self.message_type = message_type
        self.timestamp = timestamp
        self.content = content
        self.from_whom = from_whom
        self.to_whom = to_whom
        self.command = command
