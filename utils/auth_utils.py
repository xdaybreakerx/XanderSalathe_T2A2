from extensions.extensions import db
from flask import jsonify
import functools

from models.user import User

from flask_jwt_extended import get_jwt_identity


# Check if the current user has one of the specified roles.
def is_user_in_role(roles):
    # Parameters:
    # - roles: a list or tuple of roles to check against the user's role.
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # Returns:
    # - True if the user has one of the specified roles, False otherwise.
    return user.role in roles if user else False


def role_required(roles):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            stmt = db.select(User).filter_by(id=user_id)
            user = db.session.scalar(stmt)
            # Check if the user's role is in the list of allowed roles
            if user and user.role in roles:
                # Continue and run the decorated function
                return fn(*args, **kwargs)
            else:
                # Return an error if the user's role is not in the allowed list
                return jsonify({"error": "Not authorised for this action"}), 403

        return wrapper

    return decorator
