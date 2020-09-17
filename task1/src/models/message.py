from .entity import Entity
import time


class Message(Entity):

    def __init__(self,
                 message_type,
                 from_whom,
                 content=None,
                 selected_users=None,
                 command=None,
                 success=None,
                 error=None,
                 timestamp=None
                 ):
        self.message_type = message_type
        self.content = content
        self.from_whom = from_whom
        self.selected_users = selected_users
        self.command = command
        self.success = success
        self.error = error
        self.timestamp = timestamp or time.time()
