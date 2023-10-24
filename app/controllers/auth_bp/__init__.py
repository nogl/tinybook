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



