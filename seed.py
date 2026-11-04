
from app import app
from models import db, User, Note, Category


with app.app_context():
    db.drop_all()
    db.create_all()

    # Create sample users
    user1 = User(username="imran")
    user1.set_password("password123")

    user2 = User(username="john")
    user2.set_password("password123")

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create categories
    category1 = Category(name="School", user_id=user1.id)
    category2 = Category(name="Personal", user_id=user1.id)
    category3 = Category(name="Work", user_id=user2.id)

    db.session.add_all([category1, category2, category3])
    db.session.commit()

    # Create notes
    note1 = Note(
        title="Flask revision",
        content="Study Flask routes and SQLAlchemy.",
        user_id=user1.id,
        category_id=category1.id
    )

    note2 = Note(
        title="Shopping list",
        content="Buy bread, milk, and eggs.",
        user_id=user1.id,
        category_id=category2.id
    )

    note3 = Note(
        title="Project tasks",
        content="Finish the API project.",
        user_id=user1.id,
        category_id=category1.id
    )

    note4 = Note(
        title="Meeting notes",
        content="Prepare the weekly work report.",
        user_id=user2.id,
        category_id=category3.id
    )

    db.session.add_all([note1, note2, note3, note4])
    db.session.commit()

    print("Database seeded successfully!")





# ==========================================
# Responsible: Imran (Team Lead)
# File: seed.py
# Tasks:
# - Create sample database records
# - Generate sample users
# - Generate sample notes and categories
# - Populate the database for testing
# ==========================================