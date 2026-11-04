
import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-this"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///personal_notes.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False

    # Testing configuration
    TESTING = False


# ==========================================
# Responsible: Imran (Team Lead)
# File: config.py
# Tasks:
# - Configure the database connection
# - Set application configuration
# - Configure secret keys
# - Set testing configuration
# ==========================================