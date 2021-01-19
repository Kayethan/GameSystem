from flask_jwt_extended import utils
from Score.Score import Score
import datetime
from Tools.Utlis import Countries
from typing import List, Tuple
from User.User import User
from Map.MapData import MapData
from Database.Database import Database
from Tools.Settings import ILLEGAL_CHARACTERS
import re

class DatabaseHandler:
    database: Database = None

    @staticmethod
    def get_all_maps() -> List[MapData]:
        return DatabaseHandler.database.get_table("Maps").find_rows(lambda x: True)
    
    @staticmethod
    def get_map(id: str) -> MapData:
        results = DatabaseHandler.database.get_table("Maps").find_rows(lambda x: x.map_id == id)
        if len(results) == 1:
            return results[0]
        else:
            return None
    
    @staticmethod
    def add_map(map_name: str, data: str, username: str) -> str:
        for char in ILLEGAL_CHARACTERS:
            if username.find(char) != -1:
                return 6
            if data.find(char) != -1:
                return 6
            if char != " ":
                if map_name.find(char) != -1:
                    return 6

        map_data: MapData = MapData.create_from_data(None, map_name, data, username)
        
        
        if DatabaseHandler.database.get_table("Maps").add_row(map_data):
            return map_data.map_id
        else:
            return None
    
    @staticmethod
    def remove_map(id) -> bool:
        if not DatabaseHandler.database.get_table("Scores").remove_rows(lambda x: x.map_id == id):
            return False
        return DatabaseHandler.database.get_table("Maps").remove_rows(lambda x: x.map_id == id)
    
    @staticmethod
    def add_user(username: str, email: str, country: str, password: str) -> int:
        if not (country in Countries.get_list()):
            return 4
        
        for char in ILLEGAL_CHARACTERS:
            if username.find(char) != -1:
                return 6
            if email.find(char) != -1:
                return 6
            if country.find(char) != -1:
                return 6
            if password.find(char) != -1:
                return 6
        username_regex = "^[0-9a-zA-Z]+$"
        email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if re.search(email_regex, email) == None:
            return 5
        if re.search(username_regex, username) == None:
            return 6

        if len(DatabaseHandler.database.get_table("Users").find_rows(lambda x: x.username == username)) > 0:
            return 1
        elif len(DatabaseHandler.database.get_table("Users").find_rows(lambda x: x.email == email)) > 0:
            return 2
        elif len(password) < 8:
            return 3

        user = User(username, email, country)
        user.hash_password(password)

        if DatabaseHandler.database.get_table("Users").add_row(user):
            return 0
        else:
            return -1

    @staticmethod
    def get_user_username(username: str) -> User:
        results = DatabaseHandler.database.get_table("Users").find_rows(lambda x: x.username == username)
        if len(results) == 1:
            return results[0]
        else:
            return None
    
    @staticmethod
    def get_user_email(email: str) -> User:
        results = DatabaseHandler.database.get_table("Users").find_rows(lambda x: x.email == email)
        if len(results) == 1:
            return results[0]
        else:
            return None

    @staticmethod
    def add_score(username: str, map_id: str, score: int) -> int:
        if score < 1:
            return 2

        map = DatabaseHandler.database.get_table("Maps").find_rows(lambda x: x.map_id == map_id)
        if len(map) != 1:
            return 1
        today = datetime.date.today()

        sc = Score(username, map_id, score, today.year, today.month, today.day)
        for scoe in DatabaseHandler.database.get_table("Scores").find_rows(lambda x: True):
            print(str(scoe))
        DatabaseHandler.database.get_table("Scores").remove_rows(lambda x: x.user == username and x.map_id == map_id)
        if DatabaseHandler.database.get_table("Scores").add_row(sc):
            return 0
        else:
            return 3
    
    @staticmethod
    def get_user_scores(user: str) -> List[Score]:
        us = DatabaseHandler.database.get_table("Users").find_rows(lambda x: x.username == user)
        if len(us) != 1:
            return None
        
        results = DatabaseHandler.database.get_table("Scores").find_rows(lambda x: x.user == user)
        return results

    @staticmethod
    def get_scores(map: str, country: str) -> Tuple[List[Score], int]:
        mp = DatabaseHandler.database.get_table("Maps").find_rows(lambda x: x.map_id == map)
        if len(mp) != 1:
            return None, 1

        if country == "World":
            results = DatabaseHandler.database.get_table("Scores").find_rows(lambda x: x.map_id == map)
            return results, 0
        else:
            if country not in Countries.get_list():
                return None, 2
            
            users = DatabaseHandler.database.get_table("Users").find_rows(lambda x: x.country == country)
            user_names = []
            for user in users:
                user_names.append(user.username)
            results = DatabaseHandler.database.get_table("Scores").find_rows(lambda x: x.map_id == map and x.user in user_names)

            return results, 0
    
    @staticmethod
    def get_scores_mode(map: str, country: str, mode: int) -> Tuple[List[Score], int]:
        mp = DatabaseHandler.database.get_table("Maps").find_rows(lambda x: x.map_id == map)
        if len(mp) != 1:
            return None, 1

        # 0 - ALL
        # 1 - Last 365 days
        # 2 - Last 30 days
        # 3 - Last 7 days
        # 4 - Last day

        if mode < 0 or mode > 4:
            return None, 3

        if country == "World":
            # results = DatabaseHandler.database.get_table("Scores").find_rows(lambda x: x.map_id == map)
            results = None

            if mode == 0:
                results = DatabaseHandler.database.get_table("Scores").find_rows(lambda x: x.map_id == map)
            else:
                search_date = None
                if mode == 1:
                    search_date = (datetime.datetime.today() - datetime.timedelta(days = 365)).date()
                elif mode == 2:
                    search_date = (datetime.datetime.today() - datetime.timedelta(days = 30)).date()
                elif mode == 3:
                    search_date = (datetime.datetime.today() - datetime.timedelta(days = 7)).date()
                else:
                    search_date = (datetime.datetime.today() - datetime.timedelta(days = 1)).date()

                results = DatabaseHandler.database.get_table("Scores").find_rows(lambda x: x.map_id == map and x >= search_date)
            
            return results, 0
        else:
            if country not in Countries.get_list():
                return None, 2
            
            users = DatabaseHandler.database.get_table("Users").find_rows(lambda x: x.country == country)
            user_names = []
            for user in users:
                user_names.append(user.username)
            
            results = None

            if mode == 0:
                results = DatabaseHandler.database.get_table("Scores").find_rows(lambda x: x.map_id == map and x.user in user_names)
            else:
                search_date = None
                if mode == 1:
                    search_date = (datetime.datetime.today() - datetime.timedelta(days = 365)).date()
                elif mode == 2:
                    search_date = (datetime.datetime.today() - datetime.timedelta(days = 30)).date()
                elif mode == 3:
                    search_date = (datetime.datetime.today() - datetime.timedelta(days = 7)).date()
                else:
                    search_date = (datetime.datetime.today() - datetime.timedelta(days = 1)).date()

                results = DatabaseHandler.database.get_table("Scores").find_rows(lambda x: x.map_id == map and x.user in user_names and x >= search_date)

            return results, 0