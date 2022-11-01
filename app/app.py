from abc import ABC, abstractmethod
from datetime import timedelta
from urllib import response

from flask import Flask
from flask import request
from flask import jsonify
from abc import ABC, abstractmethod
from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity

from werkzeug.security import generate_password_hash, check_password_hash

#from models.user import engine
#from models.user import User

from db.connect import PostgresService
from api import api_blueprint

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'changeme'
#SECRET_KEY = 'changeme'
jwt = JWTManager(app)

'FLASK_APP=wsgi_app flask run --with-threads --reload'

# db_connection_string = 'postgresql+psycopg2://user:123qwe@0.0.0.0:5432/db_users'
# #create_engine()
# engine = create_engine(
#     db_connection_string,
#     isolation_level = "REPEATABLE READ",
#     echo=True,
# )

# print(engine)

app.register_blueprint(api_blueprint)

class AbstractCacheStorage(ABC):
    @abstractmethod
    def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    def set(self, key: str, value: str, expire: int, **kwargs):
        pass


# class Redis(AuthBaseClass):
#     #self.db = PostgresService()
#     def login(self, user, password):
#         return {}


@app.route("/auth/signin", methods=['POST'])
def sign_in():
    '''curl -X POST -H "Content-Type: application/json" -d '{"email":"test_user", "password":"123"}' http://127.0.0.1:5000/api/v1/auth/signin
        curl -X POST -H "Content-Type: application/json" -d '{"email":"test_user", "password":"123"}' http://127.0.0.1:5000/auth/signin
        url = "http://localhost:8080"
        data = {'email': 'Alice', 'password': 'ChangeMe'}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    '''
    result = request.json # or result = request.get_json(force=True)
    email = result.get('email')
    password = result.get('password')
    # token = result.get('access_token')
    #return jsonify({'email': login, 'pass': password}), 200
    #     return jsonify({"msg": "Bad username or password"}), 401
    #auth = Auth()
    #response = auth.login(login, password)

    db = PostgresService()
    print('bla bla bla')
    res = db.login(email, password)
    if not res:
        return jsonify({"error": "Invalid email or password"}), 401
    if res:
        response = dict()
        payload = dict()
        payload['email'] = email
        payload['admin'] = True
        exp_delta = timedelta(minutes=10)
        exp_refresh_delta = timedelta(days=30)
        access_token = create_access_token(email, additional_claims=payload, expires_delta=exp_delta)
        refresh_token = create_refresh_token(email, expires_delta=exp_refresh_delta)
        response['access_token'] = access_token
        response['refresh_token'] = refresh_token
        return jsonify(response), 200


@app.route('/auth/signup', methods=['POST'])
def sign_up():
    '''curl -X POST -H "Content-Type: application/json" -d '{"email":"test_user", "password":"123"}' http://127.0.0.1:5000/auth/signup'''
    result = request.json # or result = request.get_json(force=True)
    email = result.get('email')
    password = result.get('password')
    print(email)
    db = PostgresService()
    response = db.register(email, password)
    print('resp sttttttaaaa: ', response.get('status'))
    if response.get('status') == '201':
        return jsonify(response), 201
    else: 
        return jsonify(response), 403


@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True, locations=['headers'])
def refresh():
    ''' curl -X POST -H "Authorization: Bearer <refresh_token>" '''
    print(get_jwt())
    print('eto AUTH TOK', request.headers['Authorization'])
    return {}
# curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Njg4MTgxMiwianRpIjoiNDU0ODdkZmItYjE4NS00NmVmLTkxNDMtY2Y0OTYxZmIwNDNhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI5NzQ1NzZ1aTRkZ2ZnZGZnZCIsIm5iZiI6MTY2Njg4MTgxMiwiZXhwIjoxNjY5NDczODEyfQ.vQrs7N3p-QIFBFidL4jrdzqvnOnbhX7ARW0aiAXfVzs"
#      -d '{"login":"NOtoken", "password": "ssss", "access_token":"fsdfsd" }' http://127.0.0.1:5000/auth
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Njg4MTgxMiwianRpIjoiNDU0ODdkZmItYjE4NS00NmVmLTkxNDMtY2Y0OTYxZmIwNDNhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI5NzQ1NzZ1aTRkZ2ZnZGZnZCIsIm5iZiI6MTY2Njg4MTgxMiwiZXhwIjoxNjY5NDczODEyfQ.vQrs7N3p-QIFBFidL4jrdzqvnOnbhX7ARW0aiAXfVzs
# curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Njg4MTgxMiwianRpIjoiNDU0ODdkZmItYjE4NS00NmVmLTkxNDMtY2Y0OTYxZmIwNDNhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI5NzQ1NzZ1aTRkZ2ZnZGZnZCIsIm5iZiI6MTY2Njg4MTgxMiwiZXhwIjoxNjY5NDczODEyfQ.vQrs7N3p-QIFBFidL4jrdzqvnOnbhX7ARW0aiAXfVzs"
#      -d '{"login":"NOtoken", "password": "ssss", "access_token":"fsdfsd" }' http://127.0.0.1:5000/auth/refresh


# @app.route('/auth', methods=['POST'])
# @jwt_required(refresh=True, locations=['headers'])
# def auth():
#     '''curl -X POST -H "Authorization: Bearer <token>"
#      -d '{"login":"NOtoken", "password": "ssss", "access_token":"fsdfsd" }' http://127.0.0.1:5000/auth'''
#     print(request.json)
#     return {}


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8005,
        debug=True
    )

# access 
# curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjY5NDcxMCwianRpIjoiNzUyMTM4ZDctMmM0NC00ZjViLTk4MDgtODNjYjk1MDEzZmYyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImEyIiwibmJmIjoxNjY2Njk0NzEwLCJleHAiOjE2NjY2OTUzMTAsImxvZ2luIjoiYTIiLCJwYXNzd29yZCI6InRlc3Rzc3Nzc3NzIiwiYWRtaW4iOnRydWV9.kA-YrxBXV1xjcb66ulT8T_oPKH6A92KVJxRqKV-YxOk" -d '{"login":"NOtoken", "password": "ssss", "access_token":"fsdfsd" }' http://127.0.0.1:5000/auth
# refresh 
# curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjY5NDM1NSwianRpIjoiNjI2ODcyYjUtODUxYy00ZjUwLTg3MGEtOTU5NjYwZGFmZTVkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJhMiIsIm5iZiI6MTY2NjY5NDM1NSwiZXhwIjoxNjY5Mjg2MzU1fQ.O7Ip5LEGyR79nJZ_JVqqCIDF2VOBL8-50opIyCzSn5Q" -d '{"login":"NOtoken", "password": "ssss", "access_token":"fsdfsd" }' http://127.0.0.1:5000/auth