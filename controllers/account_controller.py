from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models.account import Account, account_schema, accounts_schema
from ..models.transaction import Transaction, transaction_schema, transactions_schema

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")


# http://localhost:8080/accounts - POST
@accounts_bp.route("/", methods=["POST"])
@jwt_required()
def create_account():
    body_data = request.get_json()
    account = Account(
        account_type=body_data.get("account_type"),
        balance=body_data.get("balance"),
        user_id=get_jwt_identity(),
    )
    db.session.add(account)
    db.session.commit()
    return account_schema.dump(account), 201


# http://localhost:8080/accounts - GET
@accounts_bp.route("/")
def get_all_accounts():
    stmt = db.select(Account).order_by(Account.date_created.desc())
    accounts = db.session.scalars(stmt)
    return accounts_schema.dump(accounts)


# http://localhost:8080/accounts/id - GET
@accounts_bp.route("/<int:account_id>")
def get_account(account_id):
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    if account:
        return account_schema.dump(account)
    else:
        return {"error": f"Account with id {account_id} not found"}, 404


# http://localhost:8080/accounts/id - PUT, PATCH
@accounts_bp.route("/<int:account_id>", methods=["PUT", "PATCH"])
def update_account(account_id):
    body_data = request.get_json()
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    if account:
        account.account_type = (body_data.get("account_type") or account.account_type,)
        account.balance = body_data.get("balance") or account.balance
        db.session.commit()
        return account_schema.dump(account)
    else:
        return {"error": f"Account with id {account_id} not found"}, 404


# http://localhost:8080/accounts/id - DELETE
@accounts_bp.route("/<int:account_id>", methods=["DELETE"])
@jwt_required()
def delete_account(account_id):
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    if account:
        db.session.delete(account)
        db.session.commit()
        return {"message": f"Account '{account.account_type}' deleted successfully"}
    else:
        return {"error": f"Account with id {account_id} not found"}, 404


# http://localhost:8080/accounts/id/transactions - POST
@accounts_bp.route("/<int:account_id>/transactions", methods=["POST"])
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
@accounts_bp.route(
    "/<int:account_id>/transactions/<int:transaction_id>", methods=["PUT", "PATCH"]
)
@jwt_required()
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
@accounts_bp.route(
    "/<int:account_id>/transactions/<int:transaction_id>", methods=["DELETE"]
)
@jwt_required()
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
