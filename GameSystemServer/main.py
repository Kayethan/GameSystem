import os

from flask.app import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from Database.Database import Database
from Map.MapData import MapData
from Score.Score import Score
from Server.DatabaseHandler import DatabaseHandler
from Server.Routes import initialize_routes
from Tools.Logger import Logger
from Tools.Settings import Config
from User.User import User

Config.load_config_file()
Logger.initialize()

if __name__ == "__main__":
    if os.path.exists("./.env"):
        os.environ['ENV_FILE_LOCATION'] = "./.env"
    else:
        Logger.log("Env file not present", True)

    app = Flask(__name__)
    app.config.from_envvar('ENV_FILE_LOCATION')
    api = Api(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    database = Database()
    if not database.is_good():
        Logger.log("Failed to initialize database", True)
    if not database.add_table("Users", User):
        Logger.log("Failed to initialize Users table", True)
    if not database.add_table("Maps", MapData):
        Logger.log("Failed to initialize Maps table", True)
    if not database.add_table("Scores", Score):
        Logger.log("Failed to initialize Scores table", True)

    DatabaseHandler.database = database
    
    initialize_routes(api)
    if Config.USE_SSL:
        context = (Config.CRT_PATH, Config.KEY_PATH)
        app.run(debug = Config.DEBUG, host = Config.HOSTNAME, port = Config.PORT, ssl_context = context)
    else:
        app.run(debug = Config.DEBUG, host = Config.HOSTNAME, port = Config.PORT)