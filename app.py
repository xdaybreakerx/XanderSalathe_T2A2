from os import environ

from flask import Flask

from extensions.extensions import db, ma, bcrypt, jwt
from errors.handlers import register_error_handlers


def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False
    # configs
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")

    # connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    register_error_handlers(app)

    from commands.db_commands import db_commands

    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp

    app.register_blueprint(auth_bp)

    from controllers.account_controller import accounts_bp

    app.register_blueprint(accounts_bp)
    
    from controllers.category_controller import categories_bp
    
    app.register_blueprint(categories_bp)

    return app
