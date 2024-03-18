from os import environ

from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError

from extensions.extensions import db, ma, bcrypt, jwt


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

    # Error handling 
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad Request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'Unauthorized'}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': 'Internal Server Error'}), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'message': 'Method Not Allowed'}), 405
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400
    
    from commands.db_commands import db_commands

    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp

    app.register_blueprint(auth_bp)
    
    from controllers.account_controller import accounts_bp
    
    app.register_blueprint(accounts_bp)

    return app
