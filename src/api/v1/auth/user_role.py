from datetime import timedelta
from pprint import pprint

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import abort

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity

from db.role_service import RoleService

user_role_bp = Blueprint('user_role', __name__, url_prefix='/user/role')


# TODO add JWT required to each route

@user_role_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@user_role_bp.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Request data is invalid'}), 400)


def _json_check(rrequest):
    if not rrequest.json or not 'user_id' in rrequest.json or not 'role_id' in rrequest.json:
        abort(400)


@user_role_bp.route('', methods=['GET'])
def show_user_role():
    db = RoleService()
    response_inner = [x.as_dict for x in db.user_role_show_all()]
    return jsonify({'user__roles': response_inner})


@user_role_bp.route('/user_role_add', methods=['POST'])
def user_add_role():
    _json_check(request)
    result = request.json
    user_id = result.get('user_id')
    role_id = result.get('role_id')
    db = RoleService()
    response_inner = [db.user_add_role(user_id, role_id).as_dict]
    return jsonify({'user__role created': response_inner})


@user_role_bp.route('/user_role_show/<int:user_id>', methods=['GET'])
def user_check_role(user_id):
    db = RoleService()
    response_inner = [x.as_dict for x in db.user_check_role(user_id)]
    return jsonify({'user__role': response_inner})


@user_role_bp.route('/role_user_show/<int:role_id>', methods=['GET'])
def role_check_user(role_id):
    db = RoleService()
    response_inner = [x.as_dict for x in db.role_check_user(role_id)]
    return jsonify({'role__user': response_inner})


@user_role_bp.route('/user_role_delete', methods=['DELETE'])
def user_role_remove():
    _json_check(request)
    result = request.json
    user_id = result.get('user_id')
    role_id = result.get('role_id')
    db = RoleService()
    response_inner = [db.user_remove_role(user_id, role_id).as_dict]
    return jsonify({'user__role deleted': response_inner})
