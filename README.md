# Personal Notes API

## Description

Personal Notes API is a Flask application that allows users to create and manage personal notes. Users can sign up, log in, create categories, and organise their notes. Each user can only access their own notes and categories.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-Migrate
- Flask-Bcrypt
- Marshmallow
- Flask-CORS
- Pytest

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/imranosman886-beep/personal-notes-api.git
   cd personal-notes-api
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

Run the database migrations:

```bash
flask --app app db upgrade
```

To add sample data, run:

```bash
python seed.py
```

**Note:** The seed script resets the database before adding sample data. Only run it when you are comfortable deleting existing database records.

## Running the Application

Start the Flask server:

```bash
python app.py
```

The backend runs at:

`http://localhost:5555`

## Running Tests

Run all tests using:

```bash
pytest -v
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register a new user |
| POST | `/login` | Log in |
| DELETE | `/logout` | Log out |
| GET | `/check_session` | Check login session |

### Notes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/notes` | Get all notes |
| GET | `/notes/<id>` | Get one note |
| POST | `/notes` | Create a note |
| PATCH | `/notes/<id>` | Update a note |
| DELETE | `/notes/<id>` | Delete a note |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| GET | `/categories` | Get all categories |
| GET | `/categories/<id>` | Get one category |
| POST | `/categories` | Create a category |
| PATCH | `/categories/<id>` | Update a category |
| DELETE | `/categories/<id>` | Delete a category |

## Authentication and Security

- Authentication uses Flask sessions.
- Passwords are hashed using Flask-Bcrypt.
- Protected routes require users to be logged in.
- Users can only access their own notes and categories.
- Marshmallow is used to validate and serialize data.