import enum


class MessageTypes(str, enum.Enum):
    TEXT = 'text',
    COMMAND = 'command',
    SYSTEM = 'system'

