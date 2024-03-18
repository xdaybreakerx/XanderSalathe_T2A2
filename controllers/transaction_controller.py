from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions.extensions import db
from utils.auth_utils import role_required, is_user_in_role

from models.account import Account
from models.transaction import Transaction, transaction_schema


transactions_bp = Blueprint(
    "transactions", __name__, url_prefix="/<int:account_id>/transactions"
)

# Add a new transaction
# http://localhost:8080/accounts/id/transactions - POST
@transactions_bp.route("/", methods=["POST"])
@jwt_required()
def create_transaction(account_id):
    user_id = get_jwt_identity()
    body_data = request.get_json()
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    
    # if no account is found by the id, a transaction cannot be added
    if not account:
        return {"error": f"Account with id {account_id} not found"}, 404

    # a user can only add transactions to their own account
    # a admin can add transactions to any account
    
    if is_user_in_role(["Admin"]) or int(account.user_id) == int(user_id):
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
    
    # if a user tries to add a transaction to an account they do not own, an authorization error is returned
    else:
        return {"error": "Unauthorized access"}, 403


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
