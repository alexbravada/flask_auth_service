from datetime import timedelta

from flask import Blueprint
from flask import request
from flask import jsonify
from abc import ABC, abstractmethod

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity

from db.user_service import UserService


auth_user_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_user_bp.route('/', methods=['GET', 'POST'])
def deprecated():
    return jsonify({'deprecated': 'use routes: /api/v1/auth/user/ : signin, signout, refresh, access'}), 401


@auth_user_bp.route("/signin", methods=['POST'])
def sign_in():
    return jsonify({'deprecated': 'use routes: /api/v1/auth/user/ : signin, signout, refresh, access'}), 401

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
        exp_delta = timedelta(minutes=10)
        exp_refresh_delta = timedelta(days=30)
        access_token = create_access_token(email, additional_claims=payload, expires_delta=exp_delta)
        refresh_token = create_refresh_token(email, expires_delta=exp_refresh_delta)
        response['access_token'] = access_token
        response['refresh_token'] = refresh_token
        response['resp'] = f"its from pipeline: {request.url}"
        return jsonify(response), 200


@auth_user_bp.route('/signup', methods=['POST'])
def sign_up():
    return jsonify({'deprecated': 'use routes: /api/v1/auth/user/ : signin, signout, refresh, access'}), 401

    '''curl -X POST -H "Content-Type: application/json" -d '{"email":"test_user", "password":"123"}' http://127.0.0.1:5000/api/v1/auth/user/signup'''
    result = request.json # or result = request.get_json(force=True)
    email = result.get('email')
    password = result.get('password')
    if not email or not password:
        return jsonify({'error': 'email & password require'}), 401
    db = UserService()
    response = db.register(email, password)
    print('resp sttttttaaaa: ', response.get('status'))
    if response.get('status') == '201':
        return jsonify(response), 201
    else: 
        return jsonify(response), 403


@auth_user_bp.route('/access', methods=['POST'])
@jwt_required(locations=['headers'])
def access():
    return jsonify({'deprecated': 'use routes: /api/v1/auth/user/ : signin, signout, refresh, access'}), 401

    ''' curl -X POST -H "Authorization: Bearer <refresh_token>" '''
    print(get_jwt())
    print('eto Access TOK', request.headers['Authorization'])
    return {}


@auth_user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True, locations=['headers'])
def refresh():
    return jsonify({'deprecated': 'use routes: /api/v1/auth/user/ : signin, signout, refresh, access'}), 401

    ''' curl -X POST -H "Authorization: Bearer <refresh_token>" '''
    print(get_jwt())
    print('eto AUTH TOK', request.headers['Authorization'])
    return {}
