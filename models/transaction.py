from datetime import datetime

from marshmallow import fields

from extensions.extensions import db, ma


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), nullable=False
    )  # Foreign Key

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Account
    account = db.relationship("Account", back_populates="transactions")


class TransactionSchema(ma.Schema):
    account = fields.Nested("AccountSchema", exclude=["transactions"])

    class Meta:
        fields = ("id", "amount", "description", "transaction_date", "account")
        ordered = True


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
