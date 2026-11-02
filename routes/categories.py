from flask import Blueprint, request, jsonify, session
from marshmallow import ValidationError

from models import db, Category
from serializers import CategorySchema, CategoryInputSchema


categories_bp = Blueprint("categories", __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
category_input_schema = CategoryInputSchema()


@categories_bp.route("/categories", methods=["GET"])
def get_categories():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    categories = Category.query.filter_by(user_id=user_id).all()

    return jsonify(categories_schema.dump(categories)), 200


@categories_bp.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    category = Category.query.filter_by(
        id=category_id,
        user_id=user_id
    ).first()

    if not category:
        return jsonify({"error": "Category not found"}), 404

    return jsonify(category_schema.dump(category)), 200


@categories_bp.route("/categories", methods=["POST"])
def create_category():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        category_data = category_input_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    category = Category(
        name=category_data["name"],
        user_id=user_id
    )

    db.session.add(category)
    db.session.commit()

    return jsonify(category_schema.dump(category)), 201


@categories_bp.route("/categories/<int:category_id>", methods=["PATCH"])
def update_category(category_id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    category = Category.query.filter_by(
        id=category_id,
        user_id=user_id
    ).first()

    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "A JSON object with at least one field is required"}), 400

    try:
        category_data = category_input_schema.load(data, partial=True)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    for field, value in category_data.items():
        setattr(category, field, value)

    db.session.commit()

    return jsonify(category_schema.dump(category)), 200


@categories_bp.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    category = Category.query.filter_by(
        id=category_id,
        user_id=user_id
    ).first()

    if not category:
        return jsonify({"error": "Category not found"}), 404

    # Remove the category assignment from its notes first.
    for note in category.notes:
        note.category_id = None

    db.session.delete(category)
    db.session.commit()

    return jsonify({}), 200