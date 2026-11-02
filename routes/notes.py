from flask import Blueprint, request, jsonify, session
from marshmallow import ValidationError

from models import db, Note, Category
from serializers import NoteSchema, NoteInputSchema

notes_bp = Blueprint("notes", __name__)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
note_input_schema = NoteInputSchema()






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