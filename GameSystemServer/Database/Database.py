from Database.DatabaseTable import DatabaseTable
import os
import sys

from typing import List, Dict

from Database.DatabaseTable import DatabaseTable
from Tools.Logger import Logger
from Tools.FileHandler import FileHandler

class Database:
    __DATABASE_DIR = "Data"

    def __init__(self) -> None:
        Logger.log("Initializing database...")
        self.__good = False
        if not os.path.exists(Database.__DATABASE_DIR):
            Logger.log("Creating database directory.")
            try:
                os.makedirs(Database.__DATABASE_DIR)
            except:
                Logger.log("Unable to create a data directory.", True)

        self.__tables: Dict[str, DatabaseTable] = {}
        self.__good = True
        Logger.log("Database initialized.")
    
    def is_good(self) -> bool:
        return self.__good
    
    def add_table(self, table_name, data_type: type) -> bool:
        Logger.log(f"Adding table: {table_name}")
        if table_name in self.__tables:
            Logger.log(f"There is already a table named '{table_name}' in database.")
            return False

        database_table = DatabaseTable(table_name, data_type, Database.__DATABASE_DIR)
        if not database_table.is_good():
            Logger.log(f"Table initialization failed: {table_name}")
            return False

        self.__tables[table_name] = database_table
        Logger.log(f"Table added: {table_name}")
        return True
    
    def get_table(self, table_name: str) -> DatabaseTable:
        if table_name in self.__tables:
            return self.__tables[table_name]
        else:
            Logger.log(f"There is no DatabaseTable with name '{table_name}'")
            return None
