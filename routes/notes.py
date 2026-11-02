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