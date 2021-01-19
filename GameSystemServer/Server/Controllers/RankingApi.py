from Score.Score import Score
import json

from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from Server.DatabaseHandler import DatabaseHandler
from Tools.Logger import Logger

class ScoreApi(Resource):
    @jwt_required
    def post(self):
        Logger.log("ScoreApi - POST")

        user_id = get_jwt_identity()
        user = DatabaseHandler.get_user_username(user_id)
        if user is None:
            return Response(None, mimetype="application/json", status=403)

        body = request.get_json()
        Logger.log(body)
        if "map_id" in body and "score" in body:
            map_id = str(body["map_id"])
            score = 0
            try:
                score = int(body["score"])
            except ValueError:
                return Response(json.dumps({"error": "Score must be an integer"}), mimetype="application/json", status=400)

            result = DatabaseHandler.add_score(user.username, map_id, score)
            if result == 0:
                return Response(None, status=204)
            else:
                if result == 1:
                    return Response(json.dumps({"error": "Map does not exists"}), mimetype="application/json", status=404)
                elif result == 2:
                    return Response(json.dumps({"error": "Score must be a positive number"}), mimetype="application/json", status=400)
                else:
                    return Response(json.dumps({"error": "Generic error"}), mimetype="application/json", status=400)
        else:
            return Response(None, status=400)

class ScoreUserApi(Resource):
    def get(self, user):
        Logger.log(f"ScoreUserApi - GET - user: {user}")

        user = str(user)

        scores = DatabaseHandler.get_user_scores(user)
        if scores == None:
            return Response(json.dumps({"error": "User not found"}), mimetype="application/json", status=404)
        
        results = []
        for map in scores:
            results.append(map.export_to_dict())

        return Response(json.dumps(results), mimetype="application/json", status=200)

class RankingApi(Resource):
    def get(self, map, country):
        Logger.log(f"RankingApi - GET - map: {map}, country: {country}")

        map = str(map)
        country = str(country)

        scores, error = DatabaseHandler.get_scores(map, country)

        if error == 0:
            results = []
            for score in scores:
                results.append(score.export_to_dict())

            return Response(json.dumps(results), mimetype="application/json", status=200)
        elif error == 1:
            return Response(json.dumps({"error": "Map does not exists"}), mimetype="application/json", status=404)
        elif error == 2:
            return Response(json.dumps({"error": "Country does not exists"}), mimetype="application/json", status=404)
        else:
            return Response(json.dumps({"error": "Generic error"}), mimetype="application/json", status=400)

class RankingDateApi(Resource):
    def get(self, map, country, mode):
        Logger.log(f"RankingApi - GET - map: {map}, country: {country}, mode: {mode}")

        map = str(map)
        country = str(country)
        mode = int(mode)

        scores, error = DatabaseHandler.get_scores_mode(map, country, mode)

        if error == 0:
            results = []
            for score in scores:
                results.append(score.export_to_dict())

            return Response(json.dumps(results), mimetype="application/json", status=200)
        elif error == 1:
            return Response(json.dumps({"error": "Map does not exists"}), mimetype="application/json", status=404)
        elif error == 2:
            return Response(json.dumps({"error": "Country does not exists"}), mimetype="application/json", status=404)
        elif error == 3:
            return Response(json.dumps({"error": "Invalid mode"}), mimetype="application/json", status=404)
        else:
            return Response(json.dumps({"error": "Generic error"}), mimetype="application/json", status=400)