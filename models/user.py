from datetime import datetime

from marshmallow import fields, validates
from marshmallow.validate import OneOf

from extensions import db, ma

VALID_ROLE = ("User", "Admin", "Auditor")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="User")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, onupdate=datetime.utcnow)

    accounts = db.relationship("Account", back_populates="user", cascade="all, delete")


class UserSchema(ma.Schema):
    role = fields.String(validate=OneOf(VALID_ROLE))

    accounts = fields.List(fields.Nested("AccountSchema", exclude=["user"]))

    class Meta:
        fields = (
            "id",
            "username",
            "email",
            "password_hash",
            "role",
            "date_created",
            "last_login",
            "accounts"
        )


user_schema = UserSchema(exclude=["password_hash"])
users_schema = UserSchema(many=True, exclude=["password_hash"])
