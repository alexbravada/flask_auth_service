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



user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route("/api/v1/role/add", methods=['POST'])
def add_role():
    result = request.json
    name = result.get('name')
    description = result.get('description')
    db = RoleService()
    try:
        response = db.add_role(name, description)
        return jsonify(response), 201