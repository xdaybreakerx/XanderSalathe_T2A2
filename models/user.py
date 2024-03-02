from datetime import datetime

from ..extensions import db, ma
from marshmallow import fields

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, onupdate=datetime.utcnow)

class UserSchema(ma.Schema):
    cards = fields.List(fields.Nested("CardSchema", exclude=["user"]))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["user"]))

    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "cards", "comments")


user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
