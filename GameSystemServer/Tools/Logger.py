import os
import sys
import datetime

from Tools.FileHandler import FileHandler
from Tools.Settings import Config

class Logger:
    logs_dir = ""
    log_file_prefix = "log"

    __initialized = False

    @staticmethod
    def initialize(logs_directory = "Logs"):
        if Config.DEBUG == False:
            return
        Logger.logs_dir = logs_directory

        if not os.path.exists(Logger.logs_dir):
            try:
                os.mkdir(logs_directory)
            except:
                print("Error while creating a directory.")
                print(sys.exc_info()[0])
                sys.exit(1)
        
        Logger.__initialized = True
        Logger.log("################## START OF A LOGGING SESSION ##################")
        
    @staticmethod
    def log(text, with_assert: bool = False):
        if Config.DEBUG == False:
            return
        assert(Logger.__initialized)

        today = datetime.date.today()
        print("Logging: ", text)
        if not FileHandler.write_append_to_file(
            Logger.logs_dir + "/" + Logger.log_file_prefix + "_" + str(today.year) + "_" + str(today.month) + "_" + str(today.day) + ".log",
            "[ " + str(datetime.datetime.now()) + " ] " + ("[ ERROR ] " if with_assert else "") + str(text) + "\n"
        ):
            print("Error while writing to a file.")
            print(sys.exc_info()[0])
            sys.exit(2)
        assert not with_assert
