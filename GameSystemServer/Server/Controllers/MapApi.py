from Map.MapData import MapData
import json

from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from Server.DatabaseHandler import DatabaseHandler
from Tools.Logger import Logger

class MapApi(Resource):
    def get(self):
        Logger.log("MapApi - GET")

        maps = DatabaseHandler.get_all_maps()
        result = []
        for map in maps:
            temp = map.export_to_dict()
            temp.pop("data")
            result.append(temp)
        return Response(json.dumps(result), mimetype="application/json", status=200)
    
    @jwt_required
    def post(self):
        Logger.log("MapApi - POST")

        user_id = get_jwt_identity()
        user = DatabaseHandler.get_user_username(user_id)
        if user is None:
            return Response(None, mimetype="application/json", status=403)

        body = request.get_json()
        Logger.log(body)

        if "map_name" in body and "data" in body:
            map_name = str(body["map_name"])
            data = str(body["data"])

            if len(map_name) < 1:
                return Response(json.dumps({"error": "Map_name cannot be empty"}), mimetype="application/json", status=400)
            if len(data) < 1:
                return Response(json.dumps({"error": "Data cannot be empty"}), mimetype="application/json", status=400)

            id = DatabaseHandler.add_map(map_name, data, user.username)
            if id == None:
                return Response(json.dumps({"error": "Map with given name already exists"}), mimetype="application/json", status=400)
            else:
                return Response(json.dumps({"id": id}), mimetype="application/json", status=200)
        else:
            return Response(json.dumps({"error": "Generic error"}), mimetype="application/json", status=400)

class MapIdApi(Resource):
    def get(self, id):
        Logger.log(f"MapIdApi - GET - id: {id}")

        map = DatabaseHandler.get_map(str(id))
        if map == None:
            return Response(json.dumps({"error": "Not found"}), mimetype="application/json", status=404)
        else:
            return Response(json.dumps(map.export_to_dict()), mimetype="application/json", status=200)
    
    @jwt_required
    def delete(self, id):
        Logger.log(f"MapIdApi - DELETE - id: {id}")

        user_id = get_jwt_identity()
        user = DatabaseHandler.get_user_username(user_id)
        if user in None:
            return Response(None, status=403)
        
        map: MapData = DatabaseHandler.get_map(str(id))
        if map.user != user.username:
            return Response(None, status=403)

        if DatabaseHandler.remove_map(str(id)):
            return Response(json.dumps({"id": str(id)}), mimetype="application/json", status=200)
        else:
            return Response(json.dumps({"error": "Not found"}), mimetype="application/json", status=404)
