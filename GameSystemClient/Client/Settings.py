import json
import os
from Tools.FileHandler import *

CONFIG_FILE_PATH = "./config.json"

ENTRIES_WIDTH = 20

class Config:
    DEBUG = False
    NAME = "GameSystemClient"
    USE_HTTPS = False
    HOSTNAME = "127.0.0.1"
    PORT = 5000

    GAME_EXECUT_COMMAND = "cd /d .\\Game && start /wait game.exe"
    GAME_CONFIG_PATH = ".\\Game\\config.txt"
    GAME_RESULT_PATH = ".\\Game\\result.txt"

    @staticmethod
    def load_config_file():
        data = {}
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH) as json_data_file:
                data = json.load(json_data_file)
        print(data)

        if "debug" in data:
            Config.DEBUG = bool(data["debug"])
        if "GameSystemClient" in data:
            Config.NAME = str(data["name"])
        if "use_https" in data:
            Config.USE_HTTPS = bool(data["use_https"])
        if "hostname" in data:
            Config.HOSTNAME = str(data["hostname"])
        if "port" in data:
            Config.PORT = int(data["port"])
        if "game_execut_command" in data:
            Config.GAME_EXECUT_COMMAND = str(data["game_execut_command"])
        if "game_config_path" in data:
            Config.GAME_CONFIG_PATH = str(data["game_config_path"])
        if "game_result_path" in data:
            Config.GAME_RESULT_PATH = str(data["game_result_path"])

    @staticmethod
    def get_connection_string() -> str:
        protocol = "https" if Config.USE_HTTPS else "http"
        return protocol + "://" + Config.HOSTNAME + ":" + str(Config.PORT)