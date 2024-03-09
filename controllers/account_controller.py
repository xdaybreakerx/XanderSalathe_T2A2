from flask import Blueprint

from ..extensions import db
from ..models.account import Account, accounts_schema

accounts_bp = Blueprint("accounts", __name__, url_prefix="/cards")

@accounts_bp.route("/")
def get_all_accounts():
    stmt = db.select(Account).order_by(Account.date_created.desc())
    accounts = db.session.scalars(stmt)
    return accounts_schema.dump(accounts)