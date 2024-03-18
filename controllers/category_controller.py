from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions.extensions import db
from utils.auth_utils import is_user_in_role, role_required

from models.category import Category, category_schema, categories_schema

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


# Add a new category for future transactions
# http://localhost:8080/categories - POST
@categories_bp.route("/", methods=["POST"])
@jwt_required()
def create_category():
    body_data = request.get_json()
    name = body_data.get("name")

    # check to see if this category name exists already
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({"message": "Category with this name already exists"}), 400

    if not is_user_in_role(["Auditor"]):
        category = Category(
            name=body_data.get("name"), description=body_data.get("description")
        )
        db.session.add(category)
        db.session.commit()
        return category_schema.dump(category), 201
    else:
        return {"error": "Unauthorized access"}, 403


# Get all categories
# http://localhost:8080/categories - GET
@categories_bp.route("/")
@jwt_required()
def get_all_categories():
    stmt = db.select(Category)
    categories = db.session.scalars(stmt)
    return categories_schema.dump(categories)


# Get a specific category
# http://localhost:8080/categories/id - GET
@categories_bp.route("/<int:category_id>")
@jwt_required()
def get_category(category_id):
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        return category_schema.dump(category)
    else:
        return {"error": f"Category with id {category_id} not found"}, 404


# Update an existing category for transactions
# http://localhost:8080/categories/id - PUT, PATCH
@categories_bp.route("/<int:category_id>", methods=["PUT", "PATCH"])
@jwt_required()
# Only an Admin can update a category once created
@role_required(["Admin"])
def update_category(category_id):
    body_data = request.get_json()
    new_name = body_data.get("name")
    
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    
    if not category:
        return {"error": f"Category with id {category_id} not found"}, 404
    
    # Check for another category, with the updated name excluding the current one
    if new_name and new_name != category.name:
        existing_category = Category.query.filter(
            Category.name == new_name,
            Category.id != category_id
        ).first()
        if existing_category:
            return {"error": f"A category with the name '{new_name}' already exists"}, 400
    
    category.name = body_data.get("name") or category.name
    category.description = body_data.get("description") or category.description

    db.session.commit()
    return category_schema.dump(category)
        


# http://localhost:8080/categories/id - DELETE
@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
# Only an Admin can delete a category
@role_required(["Admin"])
def delete_category(category_id):
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        db.session.delete(category)
        db.session.commit()
        return {
            "message": f"Category with id {category_id}, Name: {category.name}, and Description: {category.description}  deleted successfully"
        }
    else:
        return {"error": f"Category with id {category_id} not found"}, 404
