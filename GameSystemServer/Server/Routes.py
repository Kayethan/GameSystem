
from flask_restful import Api
from Server.Controllers.AuthApi import *
from Server.Controllers.CountriesApi import *
from Server.Controllers.MapApi import *
from Server.Controllers.RankingApi import *


def initialize_routes(api: Api):
    api.add_resource(CountriesApi, "/api/countries")

    api.add_resource(MapApi, "/api/maps")
    api.add_resource(MapIdApi, "/api/maps/<id>")

    api.add_resource(SignApi, "/api/auth/sign")
    api.add_resource(LoginApi, "/api/auth/login")

    api.add_resource(ScoreApi, "/api/score")
    api.add_resource(ScoreUserApi, "/api/score/user/<user>")
    api.add_resource(RankingApi, "/api/ranking/<map>:<country>")
    api.add_resource(RankingDateApi, "/api/ranking/<map>:<country>:<mode>")