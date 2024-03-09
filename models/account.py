from datetime import datetime

from marshmallow import fields, validates
from marshmallow.validate import OneOf

from ..extensions import db, ma


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # foreign key
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to User
    user = db.relationship("User", back_populates="accounts")


class AccountSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["username", "email"])

    class Meta:
        fields = ("account_id", "user", "account_type", "balance", "date_created")


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
