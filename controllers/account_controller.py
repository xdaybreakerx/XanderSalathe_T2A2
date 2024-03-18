from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions.extensions import db
from utils.auth_utils import is_user_in_role

from models.account import Account, account_schema, accounts_schema

from controllers.transaction_controller import transactions_bp

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")
accounts_bp.register_blueprint(transactions_bp)


# Create a new account
# http://localhost:8080/accounts - POST
@accounts_bp.route("/", methods=["POST"])
@jwt_required()
def create_account():
    body_data = account_schema.load(request.get_json())
    account = Account(
        account_type=body_data.get("account_type"),
        balance=body_data.get("balance"),
        user_id=get_jwt_identity(),
    )
    db.session.add(account)
    db.session.commit()
    return account_schema.dump(account), 201


# Get a list of all accounts
# http://localhost:8080/accounts - GET
@accounts_bp.route("/")
@jwt_required()
def get_all_accounts():
    user_id = get_jwt_identity()
    # if a user has the auditor role, they have all accounts returned to them regardless of User
    # otherwise the user has only their own accounts returned to them
    if not is_user_in_role(["Auditor"]):
        stmt = (
            db.select(Account)
            .filter_by(user_id=user_id)
            .order_by(Account.date_created.desc())
        )
        accounts = db.session.scalars(stmt)
        return accounts_schema.dump(accounts)
    stmt = db.select(Account).order_by(Account.date_created.desc())
    accounts = db.session.scalars(stmt)
    return accounts_schema.dump(accounts)


# Get a specific account
# http://localhost:8080/accounts/id - GET
@accounts_bp.route("/<int:account_id>")
@jwt_required()
def get_account(account_id):
    user_id = get_jwt_identity()
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)

    if not account:
        return {"error": f"Account with id {account_id} not found"}, 404

    # if a user has the auditor role, they can view all accounts
    # otherwise a user can only view their own account
    # if a user attempts to view an account not owned by themselves, an authorization error is returned
    if is_user_in_role(["Auditor"]) or int(account.user_id) == int(user_id):
        return account_schema.dump(account)
    else:
        return {"error": "Not authorized to view this account"}, 403


# Update an existing account
# http://localhost:8080/accounts/id - PUT, PATCH
@accounts_bp.route("/<int:account_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_account(account_id):
    user_id = get_jwt_identity()
    body_data = account_schema.load(request.get_json(), partial=True)
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)

    if not account:
        return {"error": f"Account with id {account_id} not found"}, 404

    # Only an admin can update accounts not owned by themselves,
    # if the user does not own the account they attempt to update an authorization error is returned
    if is_user_in_role(["Admin"]) or int(account.user_id) == int(user_id):
        account.account_type = (body_data.get("account_type") or account.account_type,)
        account.balance = body_data.get("balance") or account.balance
        db.session.commit()
        return account_schema.dump(account), 201
    else:
        return {"error": "Unauthorized access"}, 403


# Delete an existing account
# http://localhost:8080/accounts/id - DELETE
@accounts_bp.route("/<int:account_id>", methods=["DELETE"])
@jwt_required()
def delete_account(account_id):
    user_id = get_jwt_identity()
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)

    if not account:
        return {"error": f"Account with id {account_id} not found"}, 404

    # Only an admin can delete accounts not owned by themselves,
    # if the user does not own the account they attempt to delete an authorization error is returned
    if is_user_in_role(["Admin"]) or int(account.user_id) == int(user_id):
        db.session.delete(account)
        db.session.commit()
        return {"message": f"Account '{account.account_type}' deleted successfully"}
    else:
        return {"error": "Unauthorized access"}, 403
