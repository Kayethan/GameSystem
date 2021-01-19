import datetime
from typing import Dict, List
from Tools.Logger import Logger


class Score:
    SEPARATOR = "\t"
    PARTS_COUNT = 6

    def __init__(self, user: str, map_id: str, points: int, year: int, month: int, day: int) -> None:
        self.__user = user
        self.__map_id = map_id
        self.__points = points
        self.__year = year
        self.__month = month
        self.__day = day
    
    @classmethod
    def create_from_data(cls, user: str, map_id: str, points: int, year: int, month: int, day: int):
        return cls(user, map_id, points, year, month, day)
    
    @classmethod
    def create_from_array(cls, array: list):
        assert(len(array) == Score.PARTS_COUNT)
        return cls.create_from_data(array[0], array[1], int(array[2]), int(array[3]), int(array[4]), int(array[5]))

    @property
    def user(self):
        return self.__user

    @property
    def map_id(self):
        return self.__map_id

    @property
    def points(self):
        return self.__points

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month
        
    @property
    def day(self):
        return self.__day
    
    def __eq__(self, o: object) -> bool:
        if (isinstance(o, Score)):
            return self.map_id == o.map_id and self.user == o.user
        else:
            return super.__eq__(self, o)
    
    def __lt__(self, o: object) -> bool:
        if (isinstance(o, datetime.date)):
            dt = datetime.date(self.year, self.month, self.day)
            return dt < o
    
    def __le__(self, o: object) -> bool:
        if (isinstance(o, datetime.date)):
            dt = datetime.date(self.year, self.month, self.day)
            return dt <= o
    
    def __gt__(self, o: object) -> bool:
        if (isinstance(o, datetime.date)):
            dt = datetime.date(self.year, self.month, self.day)
            return dt > o
    
    def __ge__(self, o: object) -> bool:
        if (isinstance(o, datetime.date)):
            dt = datetime.date(self.year, self.month, self.day)
            return dt >= o
    
    def export_to_save(self) -> List:
        return [self.__user, self.__map_id, self.__points, self.year, self.month, self.day]
    
    def export_to_dict(self) -> Dict:
        return {
            "user": self.__user,
            "map_id": self.__map_id,
            "points": self.__points,
            "year": self.__year,
            "month": self.__month,
            "day": self.__day,
        }
    
    def __str__(self) -> str:
        return str(self.__user) + Score.SEPARATOR + str(self.__map_id) + Score.SEPARATOR + str(self.__points) + Score.SEPARATOR + str(self.__year) + Score.SEPARATOR + str(self.__month) + Score.SEPARATOR + str(self.day)