import datetime
import json

from flask import Response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from User.User import User
from Server.DatabaseHandler import DatabaseHandler

class SignApi(Resource):
    def post(self):
        body = request.get_json()
        if "username" in body and "email" in body and "country" in body and "password" in body:
            username = str(body["username"])
            email = str(body["email"])
            country = str(body["country"])
            password = str(body["password"])

            if len(username) < 1:
                return Response(json.dumps({"error": "Username cannot be empty"}), mimetype="application/json", status=400)
            if len(email) < 1:
                return Response(json.dumps({"error": "Email cannot be empty"}), mimetype="application/json", status=400)
            if len(country) < 1:
                return Response(json.dumps({"error": "Country cannot be empty"}), mimetype="application/json", status=400)
            if len(password) < 1:
                return Response(json.dumps({"error": "Password cannot be empty"}), mimetype="application/json", status=400)

            result = DatabaseHandler.add_user(username, email, country, password)
            if result == 0:
                return Response(None, status=204)
            else:
                if result == 1:
                    return Response(json.dumps({"error": "Username exists"}), mimetype="application/json", status=400)
                elif result == 2:
                    return Response(json.dumps({"error": "Email exists"}), mimetype="application/json", status=400)
                elif result == 3:
                    return Response(json.dumps({"error": "Bad password"}), mimetype="application/json", status=400)
                elif result == 4:
                    return Response(json.dumps({"error": "That country does not exists"}), mimetype="application/json", status=400)
                elif result == 5:
                    return Response(json.dumps({"error": "Bad email format"}), mimetype="application/json", status=400)
                elif result == 6:
                    return Response(json.dumps({"error": "Illegal characters detected"}), mimetype="application/json", status=400)
                else:
                    return Response(json.dumps({"error": "Generic error"}), mimetype="application/json", status=400)
        else:
            return Response(json.dumps({"error": "Bad model"}), mimetype="application/json", status=400)

class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        if "username" in body and "password" in body:
            username = str(body["username"])
            password = str(body["password"])
            if len(username) < 1:
                return Response(json.dumps({"error": "Username cannot be empty"}), mimetype="application/json", status=400)
            if len(password) < 1:
                return Response(json.dumps({"error": "Password cannot be empty"}), mimetype="application/json", status=400)

            user = DatabaseHandler.get_user_username(username)
            if user == None:
                return Response(json.dumps({"error": "Username or password invalid"}), mimetype="application/json", status=401)
            else:
                if user.check_password(password):
                    expires = datetime.timedelta(days=7)
                    access_token = create_access_token(identity=str(user.username), expires_delta=expires)
                    return Response(json.dumps({"token": access_token}), mimetype="application/json", status=200)
                else:
                    return Response(json.dumps({"error": "Username or password invalid"}), mimetype="application/json", status=401)
        else:
            return Response(json.dumps({"error": "Bad model"}), mimetype="application/json", status=400)