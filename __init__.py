from os import environ

from flask import Flask, jsonify
from dotenv import load_dotenv

from .extensions import db, ma, bcrypt, jwt


def create_app():
    app = Flask(__name__)

    # configs
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")

    # connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .controllers.cli_controller import db_commands

    app.register_blueprint(db_commands)

    return app
