import json
import os
from Tools.FileHandler import *

CONFIG_FILE_PATH = "./config.json"
ILLEGAL_CHARACTERS = [" ", ";","\t", "\n", "\""]

class Config:
    DEBUG = False

    USE_SSL = False
    HOSTNAME = "127.0.0.1"
    PORT = 5000

    CRT_PATH = ""
    KEY_PATH = ""

    @staticmethod
    def load_config_file():
        data = {}
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH) as json_data_file:
                data = json.load(json_data_file)
        print(data)

        if "debug" in data:
            Config.DEBUG = bool(data["debug"])
        if "use_ssl" in data:
            Config.USE_SSL = bool(data["use_ssl"])
        if "hostname" in data:
            Config.HOSTNAME = str(data["hostname"])
        if "port" in data:
            Config.PORT = int(data["port"])
        if "certificate_crt_path" in data:
            Config.CRT_PATH = str(data["certificate_crt_path"])
        if "certificate_key_path" in data:
            Config.KEY_PATH = str(data["certificate_key_path"])

    @staticmethod
    def get_connection_string() -> str:
        use_ssl = Config.USE_SSL
        return ("https" if use_ssl else "http") + "://" + Config.HOSTNAME + ":" + str(Config.PORT)