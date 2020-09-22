from .enumerator import Enumerator


class SystemTypes(Enumerator):

    NEW_USER = 'new_user'
    EXIT = 'exit'

    @staticmethod
    def list():
        return Enumerator.list(SystemTypes)