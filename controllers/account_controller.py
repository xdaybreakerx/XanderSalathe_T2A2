from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models.account import Account, accounts_schema, account_schema

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")


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


# http://localhost:8080/accounts/id - DELETE
@accounts_bp.route("/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    if account:
        db.session.delete(account)
        db.session.commit()
        return {"message": f"Account '{account.account_type}' deleted successfully"}
    else:
        return {"error": f"Account with id {account_id} not found"}, 404


# http://localhost:8080/accounts/id - PUT, PATCH
@accounts_bp.route("/<int:account_id>", methods=["PUT", "PATCH"])
def update_account(account_id):
    body_data = request.get_json()
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    if account:
        account.account_type = body_data.get("account_type") or account.account_type,
        account.balance = (body_data.get("balance") or account.balance)
        db.session.commit()
        return account_schema.dump(account)
    else:
        return {"error": f"Account with id {account_id} not found"}, 404