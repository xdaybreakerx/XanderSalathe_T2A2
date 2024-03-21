from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from extensions.extensions import db, bcrypt

from models.user import User, user_schema, users_schema

from utils.auth_utils import role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# http://localhost:8080/auth/users - GET
@auth_bp.route("/users")
@jwt_required()
@role_required(["Auditor"])
def get_all_users():
    stmt = db.select(User).order_by(User.date_created.desc())
    users = db.session.scalars(stmt)

    return users_schema.dump(users)


# http://localhost:8080/auth/register - POST
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        # data from body of POST request
        body_data = request.get_json()
        # create the User instance
        user = User(
            username=body_data.get("username"),
            email=body_data.get("email"),
        )

        # password from the POST request body
        password = body_data.get("password")
        # if password exists, hash the password, otherwise error.
        if password:
            user.password_hash = bcrypt.generate_password_hash(password).decode("UTF-8")

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409


# http://localhost:8080/auth/login - POST
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    # get the data from the request body
    body_data = request.get_json()
    # Find the user with the email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(
        user.password_hash, body_data.get("password")
    ):
        # create jwt
        token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(days=1)
        )
        # return the token along with the user info
        return {"email": user.email, "token": token, "role": user.role}
    # else
    else:
        # return error
        return {"error": "Invalid email or password"}, 401

# http://localhost:8080/auth/id - DELETE
@auth_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_required(["Admin"])
def delete_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    
    if not user:
        return {"error": f"User with id {user_id} not found"}, 404
    
    db.session.delete(user)
    db.session.commit()
    return {"message": f"User '{user.username}', '{user.role}' deleted successfully"}