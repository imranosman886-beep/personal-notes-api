from flask import Blueprint, request, jsonify, session
from marshmallow import ValidationError

from models import db, Note, Category
from serializers import NoteSchema, NoteInputSchema

notes_bp = Blueprint("notes", __name__)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
note_input_schema = NoteInputSchema()

def get_logged_in_user_id():
    return session.get("user_id")

@notes_bp.route("/notes", methods=["GET"])
def get_notes():
    user_id = get_logged_in_user_id()

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1 or per_page < 1:
        return jsonify({"error": "Page and per_page must be positive numbers"}), 400

    per_page = min(per_page, 100)

    pagination = Note.query.filter_by(user_id=user_id).order_by(
        Note.created_at.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "notes": notes_schema.dump(pagination.items),
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), 200

@notes_bp.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    user_id = get_logged_in_user_id()

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify(note_schema.dump(note)), 200


@notes_bp.route("/notes", methods=["POST"])
def create_note():
    user_id = get_logged_in_user_id()

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        note_data = note_input_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    category_id = note_data.get("category_id")

    if category_id is not None:
        category = Category.query.filter_by(
            id=category_id,
            user_id=user_id
        ).first()

        if not category:
            return jsonify({"error": "Category not found"}), 404

    note = Note(
        title=note_data["title"],
        content=note_data["content"],
        user_id=user_id,
        category_id=category_id
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(note_schema.dump(note)), 201

@notes_bp.route("/notes/<int:note_id>", methods=["PATCH"])
def update_note(note_id):
    user_id = get_logged_in_user_id()

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "A JSON object with at least one field is required"}), 400

    try:
        note_data = note_input_schema.load(data, partial=True)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    if "category_id" in note_data and note_data["category_id"] is not None:
        category = Category.query.filter_by(
            id=note_data["category_id"],
            user_id=user_id
        ).first()

        if not category:
            return jsonify({"error": "Category not found"}), 404

    for field, value in note_data.items():
        setattr(note, field, value)

    db.session.commit()

    return jsonify(note_schema.dump(note)), 200








# ==========================================
# Responsible: Abdimajid
# File: notes.py
# Tasks:
# - Implement GET notes
# - Implement GET a single note
# - Implement POST to create notes
# - Implement PATCH to update notes
# - Implement DELETE to remove notes
# - Ensure users access only their own notes
# - Implement pagination
# ==========================================