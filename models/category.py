from marshmallow import fields

from extensions.extensions import db, ma


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    # Relationship to Transaction
    transactions = db.relationship("Transaction", back_populates="category")


class CategorySchema(ma.Schema):
    transactions = fields.Nested("TransactionSchema", exclude=["categories"])

    class Meta:
        fields = ("id", "name", "description")


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
