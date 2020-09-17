import json


class Entity:

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()