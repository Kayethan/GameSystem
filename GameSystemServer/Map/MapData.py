from Tools.Logger import Logger
import uuid
from typing import Dict, List

class MapData:
    SEPARATOR = "\t"
    PARTS_COUNT = 4

    def __init__(self, map_name: str, data: str, user: str, map_id = None) -> None:
        if (map_id == None):
            self.__map_id = str(uuid.uuid1())
        else:
            self.__map_id = map_id
        self.__map_name = map_name
        self.__data = data
        self.__user = user
    
    @classmethod
    def create_from_data(cls, map_id: str, map_name: str, data: str, user: str):
        return cls(map_name, data, user, map_id)
    
    @classmethod
    def create_from_array(cls, array: list):
        assert(len(array) == MapData.PARTS_COUNT)
        return cls.create_from_data(array[0], array[1], array[2], array[3])

    @property
    def map_name(self):
        return self.__map_name

    @property
    def map_id(self):
        return self.__map_id

    @property
    def data(self):
        return self.__data

    @property
    def user(self):
        return self.__user
    
    def __eq__(self, o: object) -> bool:
        if (isinstance(o, MapData)):
            return self.map_id == o.map_id or self.map_name == o.map_name
        else:
            return super.__eq__(self, o)
    
    def export_to_save(self) -> List:
        return [self.__map_id, self.__map_name, self.__data, self.__user]
    
    def export_to_dict(self) -> Dict:
        return {
            "map_id": self.__map_id,
            "map_name": self.__map_name,
            "data": self.__data,
            "username": self.__user
        }

    def __str__(self) -> str:
        return str(self.map_id) + MapData.SEPARATOR + str(self.map_name) + MapData.SEPARATOR + str(self.__data) + MapData.SEPARATOR + str(self.__user)