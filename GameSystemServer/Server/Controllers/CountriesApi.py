from Tools.Logger import Logger
from flask_restful import Resource

from Tools.Utlis import Countries

class CountriesApi(Resource):
    def get(self):
        Logger.log("CountriesApi - GET")
        return Countries.get_list(), 200