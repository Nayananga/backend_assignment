import os

from flask import Flask

from manage import init_app
from src.blueprint import register_routing
from src.db import db
from src.extention import cors, migrate
from src.utils.auth import jwt
from src.utils.logging import configure_logging
from src.utils.principal import principal


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, supports_credentials="true", resources={r"*": {"origins": "*"}})
    principal.init_app(app)
    init_app(app)

    # Logging configuration
    configure_logging(app)

    # Register Blueprint
    register_routing(app, prefix=app.config.get("API_PREFIX"))

    return app


settings_module = os.getenv("APP_SETTINGS_MODULE")
app = create_app(settings_module)
