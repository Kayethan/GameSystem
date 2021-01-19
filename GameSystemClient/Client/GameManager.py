from Tools.Logger import Logger
from Tools.FileHandler import FileHandler
import subprocess
from Client.Settings import Config
import os

class GameManager:
    @staticmethod
    def start_game(user: str, map_name: str, map_data: str, highscore: int) -> int:
        print(user, map_data, highscore)

        if Config.GAME_EXECUT_COMMAND == "":
            return -6

        if not FileHandler.write_to_file(Config.GAME_CONFIG_PATH, f"{user}\n{map_name}\n{map_data}\n{highscore}\n"):
            return -2
        process = subprocess.Popen(Config.GAME_EXECUT_COMMAND, shell = True)
        process.wait()
        if process.returncode == 0:
            Logger.log("Game ended successfully. Exit code: 0")

            lines = FileHandler.read_from_file(Config.GAME_RESULT_PATH)
            if lines == None or lines == []:
                return -3

            if os.path.exists(Config.GAME_CONFIG_PATH):
                os.remove(Config.GAME_CONFIG_PATH)
            if os.path.exists(Config.GAME_RESULT_PATH):
                os.remove(Config.GAME_RESULT_PATH)

            try:
                result = int(lines[0])

                if result < 0:
                    return -5

                return result
            except ValueError:
                return -4
        else:
            Logger.log(f"Game ended with exit code {process.returncode}.")
            return -1
