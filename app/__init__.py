from uuid import uuid4 as uuid

from flask import Flask, request, g

from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

import json
from flask import make_response
from logging.config import dictConfig

from app import database, models
from app.base_config import BaseConfig

dictConfig(BaseConfig.LOGGING_DEFAULT_CONF)

# werkzeug_log = logging.getLogger('werkzeug')
# werkzeug_log.disabled = True

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # App Configuration
    app.config.from_object(BaseConfig)  # Load base config
    app.config.from_prefixed_env()  # Load config with prefix "FLASK_"

    migrate.init_app(app, db=database, command='database-schema')
    bcrypt.init_app(app=app)
    jwt.init_app(app=app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return models.User.query.filter_by(id=identity).one_or_none()

    @app.route('/openapi')
    def openapi():
        with open('app/tinybook_api.yml', 'r') as file:
            return file.read()

    swagger_blueprint = get_swaggerui_blueprint(
        '/openapi/docs',
        '/openapi',
        config={  # Swagger UI config overrides
            'app_name': "TinyBookApp"
        },
    )
    app.register_blueprint(swagger_blueprint)

    #  Config logging after and before each req
    @app.before_request
    def before_request_func():
        g.request_id = uuid()
        req_data = {
            "internal_trace": g.request_id,
            "remote_addr": request.remote_addr,
            "method": request.method,
            "base_url": request.base_url,
            "endpoint": request.endpoint,
            "user_agent": request.user_agent,
            "cookies": request.cookies
        }
        app.logger.info(f"INCOMING REQUEST: {json.dumps(req_data, default=str)}")

    @app.after_request
    def after_request_function(response):
        app.logger.info(f"OUTPUT RESPONSE ({g.request_id}): {response}")
        return response

    @app.route("/")
    @app.route("/index")
    def index():
        app.logger.info(f'Start index_v')
        return f'Index'

    @app.route("/cfg")  # Only available with debug mode on and environment set in development
    def get_cfg():
        app.logger.info(f'Start get_cfg')
        app.logger.info(f'{json.dumps(app.config, default=str, indent=4)}')

        if app.config.get('ENV') != 'development':
            return 'Not allowed in non development mode'
        if not app.debug:
            return 'Not allowed without debug'

        return make_response(
            json.dumps(app.config, default=str, indent=4),
            {'Content-Type': 'application/json'}
        )

    from app.controllers.app_cli import app_cli_bp
    app.register_blueprint(app_cli_bp)

    from app.controllers.auth_bp import auth_bp
    app.register_blueprint(auth_bp)

    from app.api.v1.auth import auth_api_bp
    app.register_blueprint(auth_api_bp)

    return app
