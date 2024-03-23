from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions.extensions import db
from utils.auth_utils import is_user_in_role, role_required

from models.category import Category, category_schema, categories_schema

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


# Adds a new category for future transactions if the category does not already exist.
# Accessible to all users except those with the "Auditor" role, implying auditors cannot create categories.
# http://localhost:8080/categories - POST
@categories_bp.route("/", methods=["POST"])
@jwt_required()
def create_category():
    body_data = request.get_json()
    name = body_data.get("name")

    # Query to check if a category with the given name already exists in the database.
    existing_category = Category.query.filter_by(name=name).first()
    # If the category exists, return an error message.
    if existing_category:
        return jsonify({"message": "Category with this name already exists"}), 400

    # If the user is not an Auditor, allow them to create a new category.
    if not is_user_in_role(["Auditor"]):
        category = Category(
            name=body_data.get("name"), description=body_data.get("description")
        )
        # Add the new category to the session and commit the transaction to the database.
        db.session.add(category)
        db.session.commit()
        # Return the newly created category data.
        return category_schema.dump(category), 201
    else:
        return {"error": "Unauthorized access"}, 403


# Retrieves all categories from the database.
# Accessible to all authenticated users.
# http://localhost:8080/categories - GET
@categories_bp.route("/")
@jwt_required()
def get_all_categories():
    # Query to select all categories from the database.
    stmt = db.select(Category)
    # Execute the query and retrieve the results.
    categories = db.session.scalars(stmt)
    # Return the category data.
    return categories_schema.dump(categories), 200


# Retrieves a specific category by its ID from the database.
# Accessible to all authenticated users.
# http://localhost:8080/categories/id - GET
@categories_bp.route("/<int:category_id>")
@jwt_required()
def get_category(category_id):
    # Query to select a category by its ID.
    stmt = db.select(Category).filter_by(id=category_id)
    # Execute the query and fetch the result.

    category = db.session.scalar(stmt)
    # If the category is found, return its data, otherwise return an error message.
    if category:
        return category_schema.dump(category), 200
    else:
        return {"error": f"Category with id {category_id} not found"}, 404


# Updates an existing category identified by its ID.
# Only accessible by Admin users.
# http://localhost:8080/categories/id - PUT, PATCH
@categories_bp.route("/<int:category_id>", methods=["PUT", "PATCH"])
@jwt_required()
@role_required(["Admin"])
def update_category(category_id):
    body_data = request.get_json()
    new_name = body_data.get("name")
    # Query to select the category to be updated by its ID.
    stmt = db.select(Category).filter_by(id=category_id)
    # Execute the query and fetch the result.
    category = db.session.scalar(stmt)

    # If the category does not exist, return an error message.
    if not category:
        return {"error": f"Category with id {category_id} not found"}, 404

    # Check if another category with the new name already exists, excluding the current category.
    if new_name and new_name != category.name:
        existing_category = Category.query.filter(
            Category.name == new_name, Category.id != category_id
        ).first()
        # If such a category exists, return an error message.
        if existing_category:
            return {
                "error": f"A category with the name '{new_name}' already exists"
            }, 400

    # Update the category's name and/or description if provided.
    category.name = body_data.get("name") or category.name
    category.description = body_data.get("description") or category.description

    # Commit the updates to the database.
    db.session.commit()
    # Return the updated category data.
    return category_schema.dump(category), 200


# Deletes a category identified by its ID from the database.
# Only accessible by Admin users.
# http://localhost:8080/categories/id - DELETE
@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
@role_required(["Admin"])
def delete_category(category_id):
    # Query to select the category to be deleted by its ID.
    stmt = db.select(Category).filter_by(id=category_id)
    # Execute the query and fetch the result.
    category = db.session.scalar(stmt)
    # If the category is found, delete it from the database.
    if category:
        db.session.delete(category)
        db.session.commit()
         # Return a success message.
        return {
            "message": f"Category with id {category_id}, Name: {category.name}, and Description: {category.description}  deleted successfully"
        }, 200
    else:
        return {"error": f"Category with id {category_id} not found"}, 404
