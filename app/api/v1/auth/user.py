import datetime
from pprint import pprint
import time

import json
from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity

from db.user_service import UserService
from db.token_store_service import TokenStoreService
from db.redis_base import AbstractCacheStorage
from db.token_store_service import get_token_store_service


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route("/signin", methods=['POST'])
def sign_in():
    '''
        curl -X POST -H "Content-Type: application/json" -d '{"email":"test_user", "password":"123"}' http://127.0.0.1:5000/api/v1/auth/user/signin
        url = "http://localhost:8080"
        data = {'email': 'Alice', 'password': 'ChangeMe'}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    '''
    result = request.json # or result = request.get_json(force=True)
    email = result.get('email')
    password = result.get('password')
    if not email or not password:
        return jsonify({'error': 'email & password require'}), 401
    db = UserService()
    print('bla bla bla')
    res = db.login(email, password)
    if not res:
        return jsonify({"error": "Invalid email or password"}), 401
    if res:
        response = dict()
        payload = dict()
        payload['email'] = email
        payload['admin'] = True
        exp_delta = datetime.timedelta(minutes=10)
        exp_refresh_delta = datetime.timedelta(days=30)
        access_token = create_access_token(email, additional_claims=payload, expires_delta=exp_delta)
        refresh_token = create_refresh_token(email, expires_delta=exp_refresh_delta)
        response['access_token'] = access_token
        response['refresh_token'] = refresh_token
        response['resp'] = f"its from pipeline: {request.url}"
        return jsonify(response), 200


@user_bp.route('/signup', methods=['POST'])
def sign_up():
    '''curl -X POST -H "Content-Type: application/json" -d '{"email":"test_user", "password":"123"}' http://127.0.0.1:5000/api/v1/auth/user/signup'''
    result = request.json
    email = result.get('email')
    password = result.get('password')
    db = UserService()
    response_inner = [db.register(email, password).as_dict]
    return jsonify({'registered user': response_inner}), 201


@user_bp.route('/logout', methods=['POST'])
@jwt_required(locations=['headers'])
def logout(token_store_service: AbstractCacheStorage = get_token_store_service()):
    '''curl -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{"refresh_token": "322"}' http://127.0.0.1:5000/api/v1/auth/user/logout'''
    #refresh_t = request.headers['Authorization']
    #access_t = request.json.get('access_token')
    # TODO put them into Redis Black-list
    #cache = TokenStoreService()
    #cache.add_to_blacklist('user1', {"body": "token"}, datetime.timedelta(seconds=100))
    jwt = get_jwt()
    now = int(time.time())
    print('aaa', now)
    exp = jwt.get('exp')
    print('exp', exp)
    #email = jwt.get('email')
    jti = jwt.get('jti')
    ttl = exp - now
    print('TTL', ttl)
    if ttl > 0:
        #ttl = datetime.timedelta(seconds=total)
        token_store_service.add_to_blacklist(jti, {"body": "token"}, ttl=ttl)
    print('zapisal')
    #token_in = json.loads(cache.check_blacklist('user1'))
    token_in = json.loads(token_store_service.check_blacklist(jti))
    #return {"token": str(token_in)}
    return jsonify(token_in), 200

@user_bp.route('/change_password', methods=['POST'])
@jwt_required(locations=['headers'])
def change_pwd():
    access_t = request.json.get('password')
    # TODO put them into Redis Black-list
    return {}

@user_bp.route('/access', methods=['POST'])
@jwt_required(locations=['headers'])
def access():
    ''' curl -X POST -H "Authorization: Bearer <refresh_token>" http://127.0.0.1:5000/api/v1/auth/user/access'''
    print(get_jwt())
    #print('eto Access TOK', request.headers['Authorization'])
    jwt = get_jwt()
    print('eto timestamp', jwt.get('exp'))
    return {}



@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True, locations=['headers'])
def refresh():
    ''' curl -X POST -H "Authorization: Bearer <refresh_token>" -H "Content-Type: application/json" -d '{"access_token": "token"}' http://127.0.0.1:5000/api/v1/auth/user/refresh
    '''
    print(get_jwt())
    #print('eto Refresh TOK', request.headers['Authorization'])
    access_token = request.json.get('access_token')
    jwt = get_jwt()
    ttl = jwt.get('exp')
    # TODO check access
    # TODO что то сделать с payload
    return {}
