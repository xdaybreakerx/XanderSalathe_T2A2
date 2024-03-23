from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions.extensions import db
from utils.auth_utils import role_required, is_user_in_role

from models.account import Account
from models.transaction import Transaction, transaction_schema


transactions_bp = Blueprint(
    "transactions", __name__, url_prefix="/<int:account_id>/transactions"
)


# Adds a new transaction to a specified account. This operation checks account ownership and adjusts the account balance.
# http://localhost:8080/accounts/id/transactions - POST
@transactions_bp.route("/", methods=["POST"])
@jwt_required()
def create_transaction(account_id):
    # Obtain the current user's ID from the JWT payload
    user_id = get_jwt_identity()
    body_data = request.get_json()
    # Retrieve the specified account to ensure it exists and determine if the user is authorized to add a transaction
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)

    # If no account matches the provided ID, return an error
    if not account:
        return {"error": f"Account with id {account_id} not found"}, 404

    # Allow adding transactions to an account if the user is either an admin or the account owner
    if is_user_in_role(["Admin"]) or int(account.user_id) == int(user_id):
        # Create a new Transaction object and associate it with the account
        transaction = Transaction(
            amount=body_data.get("amount"),
            description=body_data.get("description"),
            account_id=account_id,
        )
        # Add the transaction to the session and adjust the account's balance accordingly
        db.session.add(transaction)

        # Update the account balance
        account.balance += body_data.get("amount")
        db.session.add(account)

        db.session.commit()
        return transaction_schema.dump(transaction), 201

    # If the user does not own the account and is not an admin, deny access
    else:
        return {"error": "Unauthorized access"}, 403


# Updates an existing transaction, restricted to admin users. This includes adjusting the account balance if the transaction amount changes.
# http://localhost:8080/accounts/id/transactions/id - PUT, PATCH
@transactions_bp.route("/<int:transaction_id>", methods=["PUT", "PATCH"])
@jwt_required()
# Only an Admin can update a transaction
@role_required(["Admin"])
def update_transaction(account_id, transaction_id):
    body_data = request.get_json()
    # Retrieve the transaction to be updated, ensuring it exists and is part of the specified account
    stmt = db.select(Transaction).filter_by(id=transaction_id, account_id=account_id)
    transaction = db.session.scalar(stmt)
    if transaction:
        # Calculate the difference between the new amount and the original amount to adjust the account balance
        old_amount = transaction.amount
        new_amount = body_data.get("amount")

        # Update transaction details
        transaction.amount = body_data.get("amount") or transaction.amount
        transaction.description = (
            body_data.get("description") or transaction.description
        )

        # Adjust the account balance based on the amount difference
        amount_difference = new_amount - old_amount
        transaction.account.balance += amount_difference

        # Commit changes to the database
        db.session.commit()
        return transaction_schema.dump(transaction), 201
    else:
        # Return an error if the specified transaction does not exist within the given account
        return {
            "error": f"Transaction with id {transaction_id}, on account {account_id} not found"
        }, 404


# Deletes an existing transaction from an account, accessible only to admin users. This also adjusts the account's balance.
# http://localhost:8080/accounts/id/transactions/id - DELETE
@transactions_bp.route("/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
# Only an Admin can delete a transaction
@role_required(["Admin"])
def delete_transaction(account_id, transaction_id):
    # Retrieve the transaction to ensure it exists within the specified account
    stmt = db.select(Transaction).filter_by(id=transaction_id, account_id=account_id)
    transaction = db.session.scalar(stmt)
    if transaction:
        # Adjust the account's balance by subtracting the transaction's amount
        transaction.account.balance -= transaction.amount
        # Remove the transaction from the database
        db.session.delete(transaction)
        # Commit the deletion to the database
        db.session.commit()
        return {
            "message": f"Transaction with id {transaction_id}, Description: {transaction.description}, Amount: {transaction.amount} deleted successfully"
        }, 200
    else:
        # Return an error if the transaction cannot be found within the specified account
        return {
            "error": f"Transaction with id {transaction_id}, on account {account_id} not found"
        }, 404
