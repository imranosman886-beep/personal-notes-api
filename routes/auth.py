from flask import Blueprint, request, jsonify, session
from marshmallow import ValidationError

from models import db, User
from serializers import SignupSchema, LoginSchema


auth_bp = Blueprint("auth", __name__)

signup_schema = SignupSchema()
login_schema = LoginSchema()


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body is required"}), 400

    try:
        user_data = signup_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    username = user_data["username"]
    password = user_data["password"]
    password_confirmation = user_data["password_confirmation"]

    if password != password_confirmation:
        return jsonify({"error": "Passwords do not match"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "username": user.username
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body is required"}), 400

    try:
        user_data = login_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    username = user_data["username"]
    password = user_data["password"]

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session["user_id"] = user.id

        return jsonify({
            "id": user.id,
            "username": user.username
        }), 200

    return jsonify({"error": "Invalid username or password"}), 401


@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)

    return jsonify({}), 200


@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if user_id:
        user = db.session.get(User, user_id)

        if user:
            return jsonify({
                "id": user.id,
                "username": user.username
            }), 200

    return jsonify({}), 200