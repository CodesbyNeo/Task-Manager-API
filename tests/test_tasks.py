import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use an in-memory SQLite DB for tests
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)
client = TestClient(app)


# ── Helpers ───────────────────────────────────────────────────

def register_and_login(username="testuser", email="test@example.com", password="password123"):
    client.post("/auth/register", json={"username": username, "email": email, "password": password})
    response = client.post("/auth/login", data={"username": username, "password": password})
    return response.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ── Auth Tests ────────────────────────────────────────────────

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "securepass"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"


def test_register_duplicate_email():
    client.post("/auth/register", json={"username": "user1", "email": "dup@example.com", "password": "pass"})
    response = client.post("/auth/register", json={"username": "user2", "email": "dup@example.com", "password": "pass"})
    assert response.status_code == 400


def test_login_success():
    token = register_and_login("loginuser", "login@example.com", "password123")
    assert token is not None


def test_login_wrong_password():
    client.post("/auth/register", json={"username": "wrongpass", "email": "wp@example.com", "password": "correct"})
    response = client.post("/auth/login", data={"username": "wrongpass", "password": "wrong"})
    assert response.status_code == 401


# ── Task Tests ────────────────────────────────────────────────

def test_create_task():
    token = register_and_login("taskuser", "task@example.com", "pass123")
    response = client.post("/tasks/", json={"title": "Buy groceries", "priority": "high"}, headers=auth_headers(token))
    assert response.status_code == 201
    assert response.json()["title"] == "Buy groceries"


def test_get_tasks():
    token = register_and_login("listuser", "list@example.com", "pass123")
    client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers(token))
    client.post("/tasks/", json={"title": "Task 2"}, headers=auth_headers(token))
    response = client.get("/tasks/", headers=auth_headers(token))
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_update_task():
    token = register_and_login("updateuser", "update@example.com", "pass123")
    create = client.post("/tasks/", json={"title": "Old Title"}, headers=auth_headers(token))
    task_id = create.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "New Title", "completed": True}, headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["completed"] is True


def test_delete_task():
    token = register_and_login("deleteuser", "delete@example.com", "pass123")
    create = client.post("/tasks/", json={"title": "To Delete"}, headers=auth_headers(token))
    task_id = create.json()["id"]
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers(token))
    assert response.status_code == 204


def test_cannot_access_other_users_task():
    token1 = register_and_login("owner", "owner@example.com", "pass123")
    token2 = register_and_login("intruder", "intruder@example.com", "pass123")
    create = client.post("/tasks/", json={"title": "Private Task"}, headers=auth_headers(token1))
    task_id = create.json()["id"]
    response = client.get(f"/tasks/{task_id}", headers=auth_headers(token2))
    assert response.status_code == 404
