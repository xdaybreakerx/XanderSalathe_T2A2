from flask import jsonify
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

def register_error_handlers(app):
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
    
    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        return {"error": error.messages}, 400