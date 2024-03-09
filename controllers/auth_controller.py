from flask import Blueprint, request

from ..extensions import db, bcrypt
from ..models.user import User, user_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        # data from body of POST request
        body_data = request.get_json()
        # password from the POST request body
        password = body_data.get("password")
        password_hash = ""
        # if password exists, hash the password, otherwise error.
        if password:
            password_hash = bcrypt.generate_password_hash(password).decode("UTF-8")
        # create the User instance
        user = User(
            username=body_data.get("username"),
            email=body_data.get("email"),
            password_hash=password_hash,
        )

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201

    except:
        pass
