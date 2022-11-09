from datetime import timedelta
from pprint import pprint

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import abort

from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity

from db.role_service import RoleService

role_bp = Blueprint('role', __name__, url_prefix='/role')


# TODO add JWT required to each route
@role_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@role_bp.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Request data is invalid'}), 400)


@role_bp.route("/add", methods=['POST'])
def add_role():
    '''curl -X POST -H "Content-Type: application/json" -d '{"name":"role_name33", "description":"descrip"}' http://127.0.0.1:5000/api/v1/auth/role/add'''
    if not request.json or not 'name' in request.json:
        abort(400)
    result = request.json
    name = result.get('name')
    description = result.get('description')
    db = RoleService()
    response_array = [db.add_role(name, description).as_dict]
    return jsonify({'role': response_array}), 201


@role_bp.route('/delete', methods=['DELETE'])
def delete_role():
    if not request.json or not 'id' in request.json:
        abort(400)
    result = request.json
    role_id = result.get('id')
    db = RoleService()
    response_array = [db.del_role(role_id).as_dict]
    return jsonify({'deleted role': response_array})


@role_bp.route('', methods=['GET'])
def show_roles_all():
    db = RoleService()
    response_inner = [x.as_dict for x in db.show_all_roles()]
    return jsonify({'roles': response_inner})


@role_bp.route('/<int:role_id>', methods=['GET'])
def show_role(role_id):
    db = RoleService()
    response_inner = [db.show_role(role_id).as_dict]
    return jsonify({'role': response_inner})


@role_bp.route('/update', methods=['PUT'])
def update_role():
    if not request.json or not 'id' in request.json:
        abort(400)
    result = request.json
    role_id = result.get('id')
    name = result.get('name')
    description = result.get('description')
    db = RoleService()
    response_inner = [db.update_role(role_id, name, description).as_dict]
    return jsonify({'role updated': response_inner}), 201
