from datetime import datetime

from marshmallow import fields, pre_load

from extensions.extensions import db, ma

from utils.input_utils import sanitize_input


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), nullable=False
    )  # Foreign Key
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=True
    )  # Foreign Key
    # Transaction categories are optional, and as such can be nullable

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Account
    account = db.relationship("Account", back_populates="transactions")
    category = db.relationship("Category", back_populates="transactions")


class TransactionSchema(ma.Schema):
    account = fields.Nested("AccountSchema", exclude=["transactions"])
    description = fields.String()

    @pre_load
    def sanitize_data(self, data, **kwargs):
        if data.get("description"):
            data["description"] = sanitize_input(data["description"])
        return data

    class Meta:
        fields = (
            "id",
            "amount",
            "description",
            "transaction_date",
            "account",
            "category",
        )
        ordered = True


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
