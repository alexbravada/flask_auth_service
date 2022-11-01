from abc import ABC, abstractmethod
from datetime import timedelta
from urllib import response

from flask import Blueprint, Flask
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


user = Blueprint('user', __name__, url_prefix='/user')


@user.route("/signin", methods=['POST'])
def sign_in():
    '''
        curl -X POST -H "Content-Type: application/json" -d '{"mail":"test_user", "password":"123"}' http://127.0.0.1:5000/auth/signin
        url = "http://localhost:8080"
        data = {'email': 'Alice', 'password': 'ChangeMe'}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    '''
    result = request.json # or result = request.get_json(force=True)
    email = result.get('email')
    password = result.get('password')
    if not email or not password:
        return jsonify({'error': 'email & password require'}), 401
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
        response['resp'] = f"its from pipeline: {request.url}"
        return jsonify(response), 200


@user.route('/signup', methods=['POST'])
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


@user.route('/signup', methods=['POST'])
@jwt_required(locations=['headers'])
def access():
    ''' curl -X POST -H "Authorization: Bearer <refresh_token>" '''
    print(get_jwt())
    print('eto Access TOK', request.headers['Authorization'])
    return {}



@user.route('/refresh', methods=['POST'])
@jwt_required(refresh=True, locations=['headers'])
def refresh():
    ''' curl -X POST -H "Authorization: Bearer <refresh_token>" '''
    print(get_jwt())
    print('eto Refresh TOK', request.headers['Authorization'])
    return {}