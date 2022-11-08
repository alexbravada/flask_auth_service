from datetime import timedelta
from pprint import pprint

from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity

from db.role_service import RoleService


user_role_bp = Blueprint('user_role', __name__, url_prefix='/user/role')


#TODO add JWT required to each route


@user_role_bp.route('/user_role_show_all', methods=['POST', 'GET'])
def show_role():
    db = RoleService()
    response_inner = [x.as_dict for x in db.user_role_show_all()]
    return jsonify(response_inner)

@user_role_bp.route('/user_role_add', methods=['POST'])
def user_add_role():
    result = request.json
    user_id = result.get('user_id')
    role_id = result.get('role_id')
    db = RoleService()
    return db.user_add_role(user_id, role_id)


@user_role_bp.route('/user_role_show', methods=['POST'])
def user_check_role():
    result = request.json
    user_id = result.get('user_id')
    role_id = result.get('role_id')
    db = RoleService()
    response_inner = [x.as_dict for x in db.user_check_role(user_id, role_id)]
    return jsonify(response_inner)


@user_role_bp.route('/user_role_delete', methods=['POST'])
def user_role_remove():
    result = request.json
    user_id = result.get('user_id')
    role_id = result.get('role_id')
    db = RoleService()
    return db.user_remove_role(user_id, role_id)