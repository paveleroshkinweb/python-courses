import json
import struct


class Entity:

    header_struct = struct.Struct('!I')

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_bytes(self):
        json_obj = self.to_json()
        packet = json_obj.encode()
        packet_length = self.header_struct.pack(len(packet))
        return packet_length, packet

    @staticmethod
    def from_bytes(obj_bytes, cls):
        obj_json = obj_bytes.decode()
        return cls(**json.loads(obj_json))

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()