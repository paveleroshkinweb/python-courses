from .entity import Entity
import time


class Message(Entity):

    def __init__(self, message_type, from_whom, content=None, to_whom=None, command=None, success=None, error=None):
        self.message_type = message_type
        self.content = content
        self.from_whom = from_whom
        self.to_whom = to_whom
        self.command = command
        self.success = success
        self.error = error
        self.timestamp = time.time()