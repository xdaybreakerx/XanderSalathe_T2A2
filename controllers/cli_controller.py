from datetime import date

from flask import Blueprint

from ..extensions import db, bcrypt

from ..models.user import User

db_commands = Blueprint("table", __name__)


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
    db.session.commit()

    print("Tables seeded")
