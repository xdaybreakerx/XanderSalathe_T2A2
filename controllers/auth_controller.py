from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from extensions.extensions import db, bcrypt

from models.user import User, user_schema, users_schema

from utils.auth_utils import role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Retrieve all user profiles, accessible only to users with the 'Auditor' role
# http://localhost:8080/auth/users - GET
@auth_bp.route("/users")
@jwt_required()
@role_required(["Auditor"])
def get_all_users():
    # Query: Select all user records, ordering by the date they were created in descending order
    stmt = db.select(User).order_by(User.date_created.desc())
    users = db.session.scalars(stmt)
    # Return the users, serialized into JSON
    return users_schema.dump(users), 200


# Register a new user to the platform
# http://localhost:8080/auth/register - POST
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        # Extract data from the POST request's body
        body_data = request.get_json()
        # Create a new User instance with the provided username and email
        user = User(
            username=body_data.get("username"),
            email=body_data.get("email"),
        )

        # Hash the provided password and set it on the user instance
        password = body_data.get("password")
        # if password exists, hash the password, otherwise error.
        if password:
            user.password_hash = bcrypt.generate_password_hash(password).decode("UTF-8")
        # Add the new user record to the database session and commit the transaction
        db.session.add(user)
        db.session.commit()
        # Return the new user data as JSON
        return user_schema.dump(user), 201

    # Handle cases where the user could not be created due to database integrity constraints
    except IntegrityError as err:
        # A not-null constraint was violated, return an error message indicating the missing field
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}, 400
        # A unique constraint was violated, return an error message indicating the email is already in use
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409


# Authenticate a user and issue a JWT upon successful login
# http://localhost:8080/auth/login - POST
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    # Extract login credentials from the POST request's body
    body_data = request.get_json()
    # Query: Find a user record by the provided email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # Check if the user exists and the provided password is correct
    if user and bcrypt.check_password_hash(
        user.password_hash, body_data.get("password")
    ):
        # Generate a JWT token with a 1-day expiration for the authenticated user
        token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(days=1)
        )
        # Return the user's email, JWT token, and role as JSON
        return {"email": user.email, "token": token, "role": user.role}, 200
    else:
        # The email or password was invalid, return an error message
        return {"error": "Invalid email or password"}, 401


# Delete a user profile, accessible only to users with the 'Admin' role
# http://localhost:8080/auth/id - DELETE
@auth_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_required(["Admin"])
def delete_user(user_id):
    # Query: Find a user record by the provided user ID
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if not user:
        # The user record was not found, return an error message
        return {"error": f"User with id {user_id} not found"}, 404
    # Delete the found user record from the database and commit the transaction
    db.session.delete(user)
    db.session.commit()
    # Return a success message indicating the user was deleted
    return {
        "message": f"User '{user.username}', '{user.role}' deleted successfully"
    }, 200
