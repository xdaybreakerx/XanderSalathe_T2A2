from flask import Blueprint

from extensions import db, bcrypt

from models.user import User

from models.account import Account

from models.transaction import Transaction

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            username="Admin User",
            email="admin@email.com",
            password_hash=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role="Admin",
        ),
        User(
            username="User",
            email="user@email.com",
            password_hash=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role="User",
        ),
        User(
            username="Auditor",
            email="audit@email.com",
            password_hash=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role="Auditor",
        ),
    ]

    db.session.add_all(users)

    accounts = [
        Account(account_type="Savings", balance=1234.56, user=users[0]),
        Account(account_type="Credit", balance=10000.00, user=users[1]),
        Account(account_type="Holiday", balance=9876.54, user=users[2]),
    ]
    db.session.add_all(accounts)

    transactions = [
        Transaction(account=accounts[0], amount=-45.67, description="Spotify"),
        Transaction(account=accounts[1], amount=-123.45, description="Netflix"),
        Transaction(account=accounts[1], amount=-234.56, description="Leetcode"),
        Transaction(account=accounts[2], amount=-10283, description="Travel Insurance"),
    ]
    db.session.add_all(transactions)

    db.session.commit()

    print("Tables seeded")
