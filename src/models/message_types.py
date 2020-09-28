from .enumerator import Enumerator


class MessageTypes(Enumerator):

    TEXT = 'text',
    COMMAND = 'command',
    SYSTEM = 'system'

    @staticmethod
    def list():
        return Enumerator.list(MessageTypes)