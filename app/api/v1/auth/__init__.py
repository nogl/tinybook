import json

from flask import Blueprint, current_app, request, jsonify

from flask_jwt_extended import create_access_token, jwt_required, current_user

from app import database, models

current_user: models.User

auth_api_bp = Blueprint('auth_api', __name__, url_prefix="/api/v1/auth")


@auth_api_bp.route('/login', methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # user = models.User.query.filter_by(username=username).one_or_none()
    # user = database.db_session.get(models.User).where(username=username).one_or_none()
    user = models.User.query.filter(models.User.username == username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)

    return jsonify(access_token=access_token)


@auth_api_bp.route('/register', methods=["POST"])
def register():
    return 'register POST'


@auth_api_bp.route('/me')
@jwt_required()
def me():
    current_app.logger.info(f'me:{current_user.email}')
    return jsonify(loggin_as=dict(
        email=current_user.email,
        username=current_user.username,
        bio=current_user.bio
    ))
