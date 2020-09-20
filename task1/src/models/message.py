import time

from .entity import Entity


class Message(Entity):

    def __init__(self,
                 message_type,
                 sender=None,
                 system_type=None,
                 content=None,
                 selected_users=None,
                 command=None,
                 success=None,
                 ):
        self.message_type = message_type
        self.content = content
        self.sender = sender
        self.system_type = system_type
        self.selected_users = selected_users
        self.command = command
        self.success = success

    @staticmethod
    def from_bytes(obj_bytes):
        return Entity.from_bytes(obj_bytes, Message)
