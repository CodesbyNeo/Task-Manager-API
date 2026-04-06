# 📝 Task Manager API

A production-style **REST API** built with **FastAPI**, **PostgreSQL**, and **Docker**. Features JWT authentication, full CRUD operations, query filtering, and an automated CI pipeline via GitHub Actions.

---

## 🚀 Tech Stack

| Layer        | Technology              |
|-------------|--------------------------|
| Framework   | FastAPI                  |
| Database    | PostgreSQL + SQLAlchemy  |
| Auth        | JWT (python-jose)        |
| Validation  | Pydantic v2              |
| Container   | Docker + Docker Compose  |
| CI/CD       | GitHub Actions           |
| Testing     | Pytest + HTTPX           |

---

## 📦 Features

- ✅ User registration & login with hashed passwords (bcrypt)
- ✅ JWT Bearer token authentication
- ✅ Full CRUD for tasks (Create, Read, Update, Delete)
- ✅ Filter tasks by `completed` status or `priority`
- ✅ Users can only access their own tasks
- ✅ Auto-generated Swagger UI at `/docs`
- ✅ Dockerized for easy local setup
- ✅ CI pipeline runs tests on every push

---

## ⚡ Quick Start

### With Docker (recommended)

```bash
git clone https://github.com/YOUR_USERNAME/task-manager-api.git
cd task-manager-api
docker-compose up --build
```

API will be live at: `http://localhost:8000`
Swagger docs at: `http://localhost:8000/docs`

### Without Docker

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up your .env file
cp .env.example .env  # Update DATABASE_URL to point to your local PostgreSQL

uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

### Auth
| Method | Endpoint         | Description         |
|--------|-----------------|---------------------|
| POST   | /auth/register  | Register a new user |
| POST   | /auth/login     | Login, get JWT token|

### Tasks *(JWT required)*
| Method | Endpoint         | Description              |
|--------|-----------------|--------------------------|
| POST   | /tasks/         | Create a task            |
| GET    | /tasks/         | List all your tasks      |
| GET    | /tasks/{id}     | Get a specific task      |
| PUT    | /tasks/{id}     | Update a task            |
| DELETE | /tasks/{id}     | Delete a task            |

#### Query Parameters for `GET /tasks/`
- `?completed=true` — filter by completion status
- `?priority=high` — filter by priority (`low`, `medium`, `high`)

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🔐 Environment Variables

| Variable                     | Default                          | Description                |
|-----------------------------|----------------------------------|----------------------------|
| `DATABASE_URL`              | postgresql://...                 | PostgreSQL connection URL  |
| `SECRET_KEY`                | your-super-secret-key            | JWT signing secret         |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30                             | Token expiry in minutes    |

---

## 🏗️ Project Structure

```
task-manager-api/
├── app/
│   ├── main.py         # App entrypoint
│   ├── config.py       # Settings & env vars
│   ├── database.py     # DB session management
│   ├── models.py       # SQLAlchemy models
│   ├── schemas.py      # Pydantic schemas
│   ├── auth.py         # JWT logic
│   └── routers/
│       ├── users.py    # Auth endpoints
│       └── tasks.py    # Task CRUD endpoints
├── tests/
│   └── test_tasks.py   # Full test suite
├── .github/workflows/
│   └── ci.yml          # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 📄 License

MIT
