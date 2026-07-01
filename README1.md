# 🗂️ Task Manager API

A **production-ready REST API** built with FastAPI, SQLAlchemy, and JWT authentication. Manage tasks with full CRUD operations, user authentication, ownership-based authorization, automated tests, and Docker deployment.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.138-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat)](https://sqlalchemy.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## 🌐 Live Demo

> **Base URL:** `https://task-management-api-1-geo4.onrender.com/`
> 
> **Interactive Docs:** `https://task-management-api-1-geo4.onrender.com/docs`

---

## ✨ Features

- 🔐 **JWT Authentication** — secure login with Bearer tokens, BCrypt password hashing
- 👤 **User Registration & Login** — full auth flow with protected routes
- ✅ **Task CRUD** — create, read, update, delete tasks with full ownership checks
- 🔍 **Filtering & Pagination** — filter by status, priority; paginate with skip/limit
- 🛡️ **Ownership Authorization** — users can only access and modify their own tasks
- 📄 **Auto-generated Swagger Docs** — fully interactive API docs at `/docs`
- 🧪 **Automated Tests** — pytest suite covering all critical flows
- 🐳 **Docker Ready** — fully containerized with Docker + docker-compose
- ☁️ **Live Deployed** — hosted on Render with zero-downtime

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.138 |
| Language | Python 3.11 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT via python-jose + passlib/bcrypt |
| Validation | Pydantic v2 |
| Testing | pytest + httpx TestClient |
| Deployment | Docker + Render |

---

## 📁 Project Structure

```
task-manager-api/
│
├── main.py              # FastAPI app entry point, registers all routers
├── database.py          # DB connection, engine, SessionLocal, get_db
├── models.py            # SQLAlchemy ORM models (User, Task tables)
├── schemas.py           # Pydantic schemas (request/response validation)
├── utils.py             # Password hashing and verification
├── oauth2.py            # JWT creation, verification, get_current_user
├── .env                 # Environment variables (never committed)
├── Dockerfile           # Container definition
├── docker-compose.yml   # App + PostgreSQL orchestration
├── requirements.txt     # Python dependencies
│
├── routers/
│   ├── auth.py          # POST /login
│   ├── users.py         # POST /users/, GET /users/{id}
│   └── tasks.py         # Full CRUD /tasks/
│
└── tests/
    └── test_tasks.py    # pytest test suite
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Git
- Docker Desktop (optional, for containerized run)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/task-manager-api.git
cd task-manager-api
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./taskmanager.db
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

Server starts at `http://127.0.0.1:8000`  
Interactive docs at `http://127.0.0.1:8000/docs`

---

## 🐳 Run with Docker

### Using docker-compose (recommended)

```bash
docker-compose up -d
```

This starts both the FastAPI app and PostgreSQL together. Your API will be available at `http://localhost:8000`.

### Using Docker only

```bash
docker build -t task-manager-api .
docker run -p 8000:8000 task-manager-api
```

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/users/` | Register a new user | ❌ |
| `POST` | `/login` | Login and receive JWT token | ❌ |
| `GET` | `/users/{id}` | Get user by ID | ❌ |

### Tasks

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/tasks/` | Create a new task | ✅ |
| `GET` | `/tasks/` | List all your tasks | ✅ |
| `GET` | `/tasks/{id}` | Get a specific task | ✅ |
| `PATCH` | `/tasks/{id}` | Update a task | ✅ |
| `DELETE` | `/tasks/{id}` | Delete a task | ✅ |

### Query Parameters (GET /tasks/)

| Parameter | Type | Description | Example |
|---|---|---|---|
| `completed` | bool | Filter by completion status | `?completed=false` |
| `priority` | string | Filter by priority level | `?priority=high` |
| `skip` | int | Number of records to skip | `?skip=0` |
| `limit` | int | Maximum records to return | `?limit=10` |

---

## 🔐 Authentication Flow

```
1. Register   →  POST /users/        →  { email, password }
2. Login      →  POST /login         →  { access_token, token_type }
3. Use token  →  Authorization: Bearer <access_token>
4. Access     →  GET /tasks/         →  your tasks only
```

**In Postman:** After login, go to Authorization tab → Bearer Token → paste your token.  
**In Swagger:** Click the 🔒 Authorize button → paste your token → click Authorize.

---

## 📝 Example Requests

### Register a user

```json
POST /users/
{
  "email": "ahmed@example.com",
  "password": "secret123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "ahmed@example.com",
  "created_at": "2026-07-01T10:00:00Z"
}
```

### Login

```json
POST /login
{
  "email": "ahmed@example.com",
  "password": "secret123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create a task

```json
POST /tasks/
Authorization: Bearer <your_token>
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "due_date": "2026-07-05"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "high",
  "due_date": "2026-07-05",
  "created_at": "2026-07-01T10:00:00Z",
  "owner_id": 1
}
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

**Test coverage includes:**
- ✅ User registration
- ✅ User login
- ✅ Create task (authenticated)
- ✅ List tasks (authenticated)
- ✅ Update task
- ✅ Unauthenticated request blocked (401)

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | JWT signing secret — keep this private | `mysecretkey123` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes | `30` |
| `DATABASE_URL` | Database connection string | `sqlite:///./taskmanager.db` |

---

## 🔒 Security Notes

- Passwords are hashed with **BCrypt** — never stored as plain text
- JWT tokens expire after 30 minutes by default
- All task endpoints verify **ownership** — users cannot access other users' tasks
- `.env` file is excluded from git via `.gitignore`
- Always change `SECRET_KEY` before deploying to production

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Your Name**  
[GitHub](https://github.com/Zaib-un-nisa479) · [LinkedIn](https://linkedin.com/in/www.linkedin.com/in/zaib-un-nisa-a7a98b378)

---

*Built with ❤️ using FastAPI — one of the fastest Python web frameworks available*
