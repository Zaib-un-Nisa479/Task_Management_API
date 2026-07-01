# Task Manager API

A simple and secure RESTful API for managing personal tasks built with FastAPI, SQLAlchemy, and JWT authentication.

This project allows users to:
- register an account
- log in securely
- create, view, update, and delete tasks
- authenticate requests with a Bearer token

---

## Features

- User registration and login
- JWT-based authentication
- Protected task routes
- SQLite database support
- API documentation with Swagger UI and Redoc
- Automated tests for authentication and task management

---

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Python-JOSE for JWT
- Passlib with bcrypt
- SQLite
- Pytest

---

## Project Structure

```text
task-manager-api/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── oauth2.py
├── utils.py
├── routers/
│   ├── auth.py
│   ├── users.py
│   └── tasks.py
├── tests/
│   ├── test_auth.py
│   └── test_tasks.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api
```

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you are setting it up manually, install the main dependencies:

```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-dotenv pytest httpx python-multipart email-validator
```

---

## Environment Configuration

Create a `.env` file in the project root with the following values:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./taskmanager.db
```

> Replace `your_secret_key_here` with a strong secret key in production.

---

## Running the Application

Start the development server with:

```bash
uvicorn main:app --reload
```

The API will be available at:
- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

---

## API Endpoints

### Authentication

#### Register a user
```http
POST /users/
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Login
```http
POST /login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

### Tasks

#### Create task
```http
POST /tasks/
```

Headers:
```http
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "priority": "high"
}
```

#### Get all tasks
```http
GET /tasks/
```

Headers:
```http
Authorization: Bearer <access_token>
```

#### Update task
```http
PATCH /tasks/{task_id}
```

#### Delete task
```http
DELETE /tasks/{task_id}
```

---

## Authentication Flow

1. Register a user using the `/users/` endpoint.
2. Log in using the `/login` endpoint.
3. Copy the returned `access_token`.
4. Use it in the `Authorization` header as:

```http
Authorization: Bearer <access_token>
```

This token is validated by the application and used to identify the authenticated user.

---

## Testing

Run the full test suite with:

```bash
pytest tests/ -v
```

The tests cover:
- login flow
- protected endpoint access
- task creation
- task retrieval
- task updates
- unauthenticated request blocking

---

## Notes

- The application uses SQLite by default for simplicity.
- In production, consider using PostgreSQL and a stronger secret key management strategy.
- The `.env` file should not be committed to source control in production environments.

---

## License

This project is open-source and available for educational and personal use.
