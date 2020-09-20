from .enumerator import Enumerator


class SystemTypes(Enumerator):

    CREATE_NEW_USER = 'create_new_user'
    EXIT = 'exit'

    @staticmethod
    def list():
        return Enumerator.list(SystemTypes)