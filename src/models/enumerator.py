import enum


class Enumerator(str, enum.Enum):

    def __str__(self):
        return str(self.value)

    @staticmethod
    def list(enumerator):
        return [str(element) for element in enumerator]
