import time

from .entity import Entity


class Message(Entity):

    def __init__(self,
                 message_type,
                 from_whom,
                 system_type=None,
                 content=None,
                 selected_users=None,
                 command=None,
                 timestamp=None
                 ):
        self.message_type = message_type
        self.content = content
        self.from_whom = from_whom
        self.system_type = system_type
        self.selected_users = selected_users
        self.command = command
        self.timestamp = timestamp or time.time()

    @staticmethod
    def from_bytes(obj_bytes):
        return Entity.from_bytes(obj_bytes, Message)
