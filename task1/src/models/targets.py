import enum


class Targets(str, enum.Enum):
    BROADCAST = 'broadcast',
    SERVER = 'server',
