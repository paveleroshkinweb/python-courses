import json


class Entity:

    def to_json(self):
        return json.dumps(self.__dict__)