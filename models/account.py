from datetime import datetime

from marshmallow import fields, pre_load
from marshmallow.validate import Length, And, Regexp

from extensions.extensions import db, ma

from utils.input_utils import sanitize_input


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # foreign key

    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="accounts")
    transactions = db.relationship(
        "Transaction", back_populates="account", cascade="all, delete"
    )


class AccountSchema(ma.Schema):

    account_type = fields.String(
        validate=And(
            Length(min=2, error="Title must be at least 2 characters long"),
            Regexp(
                "^[a-zA-Z0-9 ]+$", error="Title can only have alphanumeric characters"
            ),
        ),
    )

    user = fields.Nested("UserSchema", only=["username", "email"])

    transactions = fields.List(
        fields.Nested("TransactionSchema", only=("id", "amount", "description"))
    )

    @pre_load
    def sanitize_data(self, data, **kwargs):
        # Sanitize the account_type field
        if data.get("account_type"):
            data["account_type"] = sanitize_input(data["account_type"])
        return data

    class Meta:
        fields = (
            "id",
            "account_type",
            "balance",
            "transactions",
            "date_created",
            "user",
        )
        ordered = True


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
