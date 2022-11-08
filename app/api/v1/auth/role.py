from datetime import timedelta
from pprint import pprint

from flask import Blueprint
from flask import request
from flask import jsonify


from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity

from db.role_service import RoleService


role_bp = Blueprint('role', __name__, url_prefix='/role')


#TODO add JWT required to each route


@role_bp.route("/add", methods=['POST'])
def add_role():
    '''curl -X POST -H "Content-Type: application/json" -d '{"name":"role_name33", "description":"descrip"}' http://127.0.0.1:5000/api/v1/auth/role/add'''
    result = request.json
    name = result.get('name')
    description = result.get('description')
    db = RoleService()
    response = db.add_role(name, description)
    print(response)
    return response, 201


@role_bp.route('/delete', methods=['POST'])
def delete_role():
    result = request.json
    role_id = result.get('id')
    db = RoleService()
    return db.del_role(role_id)


@role_bp.route('/show_all', methods=['POST', 'GET'])
def show_roles_all():
    db = RoleService()
    response_inner = [x.as_dict for x in db.show_all_roles()]
    return jsonify(response_inner)


@role_bp.route('/show', methods=['POST', 'GET'])
def show_role():
    result = request.json
    role_id = result.get('id')
    db = RoleService()
    response_inner = [x.as_dict for x in db.show_role(role_id)]
    return jsonify(response_inner)


@role_bp.route('/update', methods=['POST'])
def update_role():
    result = request.json
    role_id = result.get('id')
    name = result.get('name')
    description = result.get('description')
    db = RoleService()
    return db.update_role(role_id, name, description)
