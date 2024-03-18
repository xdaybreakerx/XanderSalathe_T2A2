from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions.extensions import db
from utils.auth_utils import role_required, is_user_in_role

from models.account import Account
from models.transaction import Transaction, transaction_schema
from models.user import User


transactions_bp = Blueprint(
    "transactions", __name__, url_prefix="/<int:account_id>/transactions"
)


# http://localhost:8080/accounts/id/transactions - POST
@transactions_bp.route("/", methods=["POST"])
@jwt_required()
def create_transaction(account_id):
    body_data = request.get_json()
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    if account:
        transaction = Transaction(
            amount=body_data.get("amount"),
            description=body_data.get("description"),
            account_id=account_id,
        )
        db.session.add(transaction)

        account.balance += body_data.get("amount")
        db.session.add(account)

        db.session.commit()
        return transaction_schema.dump(transaction), 201
    else:
        return {"error": f"Account with id {account_id} not found"}, 404


# http://localhost:8080/accounts/id/transactions/id - PUT, PATCH
@transactions_bp.route("/<int:transaction_id>", methods=["PUT", "PATCH"])
@jwt_required()
# Only an Admin can update a transaction
@role_required(["Admin"])
def update_transaction(account_id, transaction_id):
    body_data = request.get_json()
    stmt = db.select(Transaction).filter_by(id=transaction_id, account_id=account_id)
    transaction = db.session.scalar(stmt)
    if transaction:
        old_amount = transaction.amount
        new_amount = body_data.get("amount")

        transaction.amount = body_data.get("amount") or transaction.amount
        transaction.description = (
            body_data.get("description") or transaction.description
        )

        amount_difference = new_amount - old_amount
        transaction.account.balance += amount_difference

        db.session.commit()
        return transaction_schema.dump(transaction)
    else:
        return {
            "error": f"Transaction with id {transaction_id}, on account {account_id} not found"
        }, 404


# http://localhost:8080/accounts/id/transactions/id - DELETE
@transactions_bp.route("/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
# Only an Admin can delete a transaction
@role_required(["Admin"])
def delete_transaction(account_id, transaction_id):
    stmt = db.select(Transaction).filter_by(id=transaction_id, account_id=account_id)
    transaction = db.session.scalar(stmt)
    if transaction:
        transaction.account.balance -= transaction.amount
        db.session.delete(transaction)
        db.session.commit()
        return {
            "message": f"Transaction with id {transaction_id}, Description: {transaction.description}, Amount: {transaction.amount} deleted successfully"
        }
    else:
        return {
            "error": f"Transaction with id {transaction_id}, on account {account_id} not found"
        }, 404
