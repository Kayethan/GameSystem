import os
import sys

from typing import Any, List, Callable, AnyStr

from Tools.Logger import Logger
from Tools.FileHandler import FileHandler

class DatabaseTable:
    __DATABASE_TABLE_FILE_EXTENSION = ".db"
    __DATA_SEPARATOR = ";"

    def __init__(self, table_name: str, data_type: type, db_dir: str) -> None:
        Logger.log(f"Initializing table {table_name}...")
        self.__good = False

        self.__accept_type = data_type
        self.__table_name = table_name
        self.__data_rows = []

        self.__file_path = f"{db_dir}/{self.__table_name}{DatabaseTable.__DATABASE_TABLE_FILE_EXTENSION}"
        self.__good = self.load_data_from_file()
        if self.__good:
            Logger.log(f"Table {table_name} initialized.")
        else:
            Logger.log(f"Table {table_name} falied to initialize.")
    
    def is_good(self) -> bool:
        return self.__good
    
    def load_data_from_file(self) -> bool:
        self.__data_rows = []
        Logger.log(f"Loading data for '{self.__table_name}' table from '{self.__file_path}'.")

        if os.path.exists(self.__file_path):
            lines = FileHandler.read_from_file(self.__file_path)
            if (lines != None):
                for line in lines:
                    if len(line) > 0:
                        try:
                            self.__data_rows.append(self.__accept_type.create_from_array(line.rstrip("\n").split(DatabaseTable.__DATA_SEPARATOR)))
                        except AssertionError:
                            Logger.log("Data corruption", True)
                            return False
            else:
                Logger.log(f"File {self.__file_path} load failed.")
                return False
        
        Logger.log(f"Loading data for '{self.__table_name}' table from '{self.__file_path}' has ended.")
        return True
    
    def save_data_to_file(self) -> bool:
        Logger.log(f"Saving data of '{self.__table_name}' table to '{self.__file_path}'.")

        data_to_save = ""
        for data in self.__data_rows:
            data_to_save += DatabaseTable.__DATA_SEPARATOR.join(str(x) for x in data.export_to_save())

            data_to_save += "\n"
        
        return FileHandler.write_to_file(self.__file_path, data_to_save)

    def add_row(self, data) -> bool:
        Logger.log(f"Adding '{str(data)}' to '{self.__table_name}' table.")

        if not isinstance(data, self.__accept_type):
            Logger.log(f"Incorrect data type. Was '{str(type(data))}', but '{str(self.__accept_type)}' was expected.")
            return False

        for temp in self.__data_rows:
            if data == temp:
                Logger.log(f"There is already object '{str(data)}' in the table.")
                return False

        self.__data_rows.append(data)
        if not self.save_data_to_file():
            Logger.log(f"'{self.__table_name}' table save failed.", True)
            return False
        
        Logger.log(f"Data added successfuly to table '{self.__table_name}'")
        return True
    
    def remove_row(self, data) -> bool:
        Logger.log(f"Removing '{str(data)}' from '{self.__table_name}' table.")
        if not isinstance(data, self.__accept_type):
            Logger.log(f"Incorrect data type. Was '{str(type(data))}', but '{str(self.__accept_type)}' was expected.", True)

        found = False
        for row in self._data_rows:
            if row == data:
                self._data_rows.remove(row)
                found = True
        
        if found:
            if not self.save_data_to_file():
                Logger.log(f"'{self.__table_name}' table save failed.", True)
                return False
            Logger.log(f"Data removed successfuly from table '{self.__table_name}'.")
        else:
            Logger.log(f"Data not found in table '{self.__table_name}'.")
            return False
            
        return found
    
    def remove_rows(self, predicat: Callable[[Any], bool]) -> bool:
        flag = False

        for data in list(filter(predicat, self.__data_rows)):
            flag = True
            Logger.log(f"Removed '{str(data)}'' from table '{self.__table_name}'.")
            self.__data_rows.remove(data)
        
        if flag:
            if not self.save_data_to_file():
                Logger.log(f"'{self.__table_name}' table save failed.", True)
                return False
            Logger.log(f"Data removed successfuly from table '{self.__table_name}'.")
        else:
            Logger.log(f"No data found in table '{self.__table_name}'.")
        
        return True
    
    def find_rows(self, predicat: Callable[[Any], bool]):
        if not self.load_data_from_file():
            Logger.log(f"'{self.__table_name}' table save failed.", True)
            return None
        return list(filter(predicat, self.__data_rows))

    @property
    def table_name(self):
        return self.__table_name