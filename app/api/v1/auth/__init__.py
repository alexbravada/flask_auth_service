from flask import Blueprint
from .user import user_bp

auth_dir_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_dir_bp.register_blueprint(user_bp)
