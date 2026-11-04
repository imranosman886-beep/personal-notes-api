
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from models import db, bcrypt
from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.categories import categories_bp


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    CORS(
        app,
        origins=["http://localhost:4000"],
        supports_credentials=True
    )

    db.init_app(app)
    bcrypt.init_app(app)

    Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(categories_bp)

    @app.route("/")
    def home():
        return jsonify({"message": "Personal Notes API is running"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(port=5555, debug=True)



# ==========================================
# Responsible: Imran (Team Lead)
# File: app.py
# Tasks:
# - Initialise the Flask application
# - Configure the application
# - Register application routes
# - Handle application errors
# ==========================================