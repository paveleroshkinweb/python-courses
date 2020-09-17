from .entity import Entity


class User(Entity):

    def __init__(self, name):
        self.name = name
