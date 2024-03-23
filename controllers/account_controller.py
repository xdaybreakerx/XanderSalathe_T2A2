from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from extensions.extensions import db
from utils.auth_utils import is_user_in_role, role_required

from models.account import Account, account_schema, accounts_schema
from models.transaction import Transaction, transactions_schema

from controllers.transaction_controller import transactions_bp

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")
accounts_bp.register_blueprint(transactions_bp)


# Used to create a new Account in relation to a User
# http://localhost:8080/accounts - POST
@accounts_bp.route("/", methods=["POST"])
@jwt_required()
def create_account():
    # Load JSON data from the request
    body_data = account_schema.load(request.get_json())
    # Instantiate a new Account model using the provided data
    account = Account(
        account_type=body_data.get("account_type"),
        balance=body_data.get("balance"),
        user_id=get_jwt_identity(),
    )
    # Add the new account to the session and commit to the database
    db.session.add(account)
    db.session.commit()
    # Return the newly created account details as a JSON object
    return account_schema.dump(account), 201


# Get a list of all accounts
# http://localhost:8080/accounts - GET
@accounts_bp.route("/")
@jwt_required()
def get_all_accounts():
    user_id = get_jwt_identity()
    # Query all accounts if the user is an auditor; otherwise, filter by the user's ID
    if not is_user_in_role(["Auditor"]):
        # Select all accounts where the user ID matches the logged-in user, ordered by creation date
        stmt = (
            db.select(Account)
            .filter_by(user_id=user_id)
            .order_by(Account.date_created.desc())
        )
        accounts = db.session.scalars(stmt)
        return accounts_schema.dump(accounts), 200
    # Select all accounts, ordered by creation date, without filtering by user ID
    stmt = db.select(Account).order_by(Account.date_created.desc())
    accounts = db.session.scalars(stmt)
    # Execute the query and return the results
    return accounts_schema.dump(accounts), 200


# Get a specific account
# http://localhost:8080/accounts/id - GET
@accounts_bp.route("/<int:account_id>")
@jwt_required()
def get_account(account_id):
    # Select an account by its ID
    user_id = get_jwt_identity()
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    # If the account does not exist, return an error message
    if not account:
        return {"error": f"Account with id {account_id} not found"}, 404

    # If the user is an auditor or the owner of the account, return account details; otherwise, return an error
    if is_user_in_role(["Auditor"]) or int(account.user_id) == int(user_id):
        return account_schema.dump(account), 200
    else:
        return {"error": "Not authorized to view this account"}, 403


# Update an existing account
# http://localhost:8080/accounts/id - PUT, PATCH
@accounts_bp.route("/<int:account_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_account(account_id):
    user_id = get_jwt_identity()
    # Partially load JSON data allowing for optional fields
    body_data = account_schema.load(request.get_json(), partial=True)
    # Select an account by its ID
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    # If the account does not exist, return an error message
    if not account:
        return {"error": f"Account with id {account_id} not found"}, 404
    # If the user is an admin or the owner of the account, update the account details; otherwise, return an error
    if is_user_in_role(["Admin"]) or int(account.user_id) == int(user_id):
        account.account_type = (body_data.get("account_type") or account.account_type,)
        account.balance = body_data.get("balance") or account.balance
        # Commit the updates to the database
        db.session.commit()
        return account_schema.dump(account), 201
    else:
        return {"error": "Unauthorized access"}, 403


# Delete an existing account
# http://localhost:8080/accounts/id - DELETE
@accounts_bp.route("/<int:account_id>", methods=["DELETE"])
@jwt_required()
def delete_account(account_id):
    # Select an account by its ID
    user_id = get_jwt_identity()
    stmt = db.select(Account).filter_by(id=account_id)
    account = db.session.scalar(stmt)
    # If the account does not exist, return an error message
    if not account:
        return {"error": f"Account with id {account_id} not found"}, 404
    # If the user is an admin or the owner of the account, delete the account; otherwise, return an error
    if is_user_in_role(["Admin"]) or int(account.user_id) == int(user_id):
        # Remove the account from the database
        db.session.delete(account)
        # Commit the changes to the database
        db.session.commit()
        return {
            "message": f"Account '{account.account_type}' deleted successfully"
        }, 200
    else:
        return {"error": "Unauthorized access"}, 403


# Retrieve the total balance from all accounts, only accessible by users with "Auditor" role.
# http://localhost:8080/accounts/total_balance - GET
@accounts_bp.route("/total_balance")
@jwt_required()
@role_required(["Auditor"])
def total_balance():
    # This query calculates the sum of balances across all accounts in the database.
    total = db.session.query(func.sum(Account.balance)).scalar()
    return jsonify({"total_balance": total}), 200


# Rank transactions within an account by their amounts in descending order, accessible only by "Auditor".
# http://localhost:8080/accounts/id/transactions/rank - GET
@accounts_bp.route("/<int:account_id>/transactions/rank")
@jwt_required()
@role_required(["Auditor"])
def transaction_ranks(account_id):
    # This query assigns a rank to each transaction within a specified account based on the transaction amount.
    # It uses a window function to order transactions by amount within the partition of the account.
    ranked_transactions = (
        db.session.query(
            Transaction.id,
            Transaction.amount,
            func.rank()
            .over(
                order_by=Transaction.amount.desc(), partition_by=Transaction.account_id
            )
            .label("rank"),
        )
        .filter(Transaction.account_id == account_id)
        .all()
    )
    # The result is formatted into a list of dictionaries, each representing a transaction with its rank.
    results = [
        {"transaction_id": t.id, "amount": str(t.amount), "rank": t.rank}
        for t in ranked_transactions
    ]
    return jsonify(results), 200


# Provide a summary of accounts with the total amount spent per account, only for "Auditor".
# http://localhost:8080/accounts/summary - GET
@accounts_bp.route("/summary")
@jwt_required()
@role_required(["Auditor"])
def account_summary():
    # This query creates a Common Table Expression (CTE) named 'account_summary' that contains
    # the total amount spent per account. It groups the sum of transaction amounts by account ID.
    cte = (
        db.session.query(
            Account.id.label("account_id"),
            func.sum(Transaction.amount).label("total_spent"),
        )
        .join(Transaction)
        .group_by(Account.id)
        .cte(name="account_summary")
    )
    # It then joins the CTE with the accounts table to get the account types along with the calculated total spent.
    summary = (
        db.session.query(cte.c.account_id, Account.account_type, cte.c.total_spent)
        .join(Account, Account.id == cte.c.account_id)
        .all()
    )
    # The final result is a list of account summaries, each including the account ID, type, and total spent.
    return (
        jsonify(
            [
                {
                    "account_id": row.account_id,
                    "account_type": row.account_type,
                    "total_spent": row.total_spent,
                }
                for row in summary
            ]
        )
    ), 200


# Search for transactions based on a description term, with role-based results filtering.
# http://localhost:8080/accounts/search - POST
@accounts_bp.route("/search", methods=["POST"])
@jwt_required()
def transactions_search():
    # Retrieves the search term from the request body and ensures it is provided.
    body_data = request.get_json()
    if not body_data or "query" not in body_data:
        return jsonify({"error": "Search term is required"}), 400

    user_id = get_jwt_identity()
    search_term = f"%{body_data['query']}%"
    # The query joins transactions with accounts and filters transactions by the search term using a case-insensitive LIKE.
    query = Transaction.query.join(Account).filter(
        Transaction.description.ilike(search_term)
    )

    # If the user is an auditor, they see all transactions. Otherwise, they only see transactions from their accounts.
    if is_user_in_role("Auditor"):
        search_result = query.all()
        return jsonify(transactions_schema.dump(search_result)), 200
    else:
        user_results = query.filter(Account.user_id == user_id)
        # Returns a JSON array of transactions that match the search term.
        return jsonify(transactions_schema.dump(user_results)), 200
