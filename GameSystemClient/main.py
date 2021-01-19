from Client.Settings import Config
from Tools.Logger import Logger
from Client.LoginWindow import LoginWindow
from Client.MainWindow import MainWindow

def run():
    Config.load_config_file()
    Logger.initialize()
    
    login = LoginWindow()
    login.show()

    token = login.token

    if token == "":
        Logger.log("Canceled. Closing...")
        return
    Logger.log("Logged as: " + login.username)
    
    MainWindow(token, login.username)

if __name__ == "__main__":
    run()