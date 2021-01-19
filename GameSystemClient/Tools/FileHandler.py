import os
import sys
import io
from typing import List

class FileHandler:
    @staticmethod
    def write_append_to_file(path: str, text: str) -> bool:
        return FileHandler._save_to_file(path, "a", text)
    
    @staticmethod
    def write_to_file(path: str, text: str) -> bool:
        return FileHandler._save_to_file(path, "w", text)

    @staticmethod
    def read_from_file(path: str) -> List[str]:
        return FileHandler._load_from_file_get_list(path, "r")

    @staticmethod
    def _save_to_file(path, mode, text) -> bool:
        # try:
        #     f = open(path, mode)
        #     f.write(text)
        #     f.close()
        # except:
        #     return False
        # return True
        try:
            with io.open(path, mode, encoding='utf8') as f:
                f.write(text)
                f.close()
        except:
            return False
        return True
            
    
    @staticmethod
    def _load_from_file_get_list(path, mode) -> List[str]:
        cont = []
        # try:
        #     f = open(path, mode)
        #     cont = f.readlines()
        #     f.close()
        # except:
        #     return None
        # return cont
        try:
            with io.open(path, mode, encoding='utf8') as f:
                cont = f.readlines()
                f.close()
        except:
            return None
        return cont
