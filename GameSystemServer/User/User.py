from typing import Dict, List
from flask_bcrypt import generate_password_hash, check_password_hash
from Tools.Logger import Logger

class User:
    SEPARATOR = "\t"
    PARTS_COUNT = 4

    def __init__(self, username: str, email: str, country: str, password: str = None) -> None:
        self.__username = username
        self.__email = email
        self.__country = country
        self.__password = password
    
    @classmethod
    def create_from_data(cls, username: str, email: str, country: str, password: str):
        assert(username != None)
        assert(email != None)
        assert(country != None)
        assert(password != None)
        return cls(username, email, country, password)
    
    @classmethod
    def create_from_array(cls, array: list):
        assert(len(array) == User.PARTS_COUNT)
        return cls.create_from_data(array[0], array[1], array[2], array[3])

    @property
    def username(self):
        return self.__username
    
    @property
    def email(self):
        return self.__email
    
    @property
    def country(self):
        return self.__country

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.username == o.username or self.email == o.email
        else:
            return super.__eq__(self, o)

    def export_to_save(self) -> List:
        return [self.__username, self.__email, self.__country, self.__password]
    
    def export_to_dict(self) -> Dict:
        return {
            "username": self.__username,
            "email": self.__email,
            "country": self.__country
        }
    
    def __str__(self) -> str:
        return self.__username + User.SEPARATOR + self.__email + User.SEPARATOR + self.__country

    def hash_password(self, password: str):
        self.__password = generate_password_hash(password).decode("utf8")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.__password, password)