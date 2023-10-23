import json

from flask import Blueprint, current_app
from app import database, models

from flask_jwt_extended import jwt_required, current_user

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.route('/login')
def login():
    return 'login page'


@auth_bp.route('/register')
def register():
    return 'register page'


@auth_bp.route('/me')
@jwt_required()
def me():
    current_app.logger.info(f'me:{current_user.email}')
    return f'me page {current_user.email}\n'
