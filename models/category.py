from marshmallow import fields, pre_load
from marshmallow.validate import Length, And, Regexp

from extensions.extensions import db, ma

from utils.input_utils import sanitize_input


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    # Relationship to Transaction
    transactions = db.relationship("Transaction", back_populates="category")


class CategorySchema(ma.Schema):

    name = fields.String(
        validate=And(
            Length(min=2, error="Category name must be at least 2 characters long"),
            Regexp(
                "^[a-zA-Z0-9 ]+$",
                error="Category name can only have alphanumeric characters",
            ),
        ),
    )
    transactions = fields.Nested("TransactionSchema", exclude=["categories"])

    @pre_load
    def sanitize_data(self, data, **kwargs):
        if data.get("name"):
            data["name"] = sanitize_input(data["name"])
        if data.get("description"):
            data["description"] = sanitize_input(data["description"])
        return data

    class Meta:
        fields = ("id", "name", "description")


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
