from fastapi.testclient import TestClient
from main import app
from database import engine, SessionLocal
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

client = TestClient(app)


def setup_function():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

# ── helpers ───────────────────────────────────
def register_and_login():
    client.post("/users/", json={"email":"test@test.com","password":"secret123"})
    res = client.post("/login", json={"email":"test@test.com","password":"secret123"})
    return res.json()["access_token"]

def auth_headers():
    token = register_and_login()
    return {"Authorization": f"Bearer {token}"}

# ── tests ─────────────────────────────────────
def test_register():
    res = client.post("/users/", json={"email":"new@test.com","password":"pass123"})
    assert res.status_code == 201
    assert res.json()["email"] == "new@test.com"
    assert "password" not in res.json()  # password never returned

def test_login():
    client.post("/users/", json={"email":"login@test.com","password":"pass123"})
    res = client.post("/login", json={"email":"login@test.com","password":"pass123"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_create_task():
    res = client.post("/tasks/", json={"title":"Test task"}, headers=auth_headers())
    assert res.status_code == 201
    assert res.json()["title"] == "Test task"

def test_get_tasks():
    headers = auth_headers()
    client.post("/tasks/", json={"title":"Task 1"}, headers=headers)
    res = client.get("/tasks/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_update_task():
    headers = auth_headers()
    created = client.post("/tasks/", json={"title":"Old title"}, headers=headers)
    task_id = created.json()["id"]
    res = client.patch(f"/tasks/{task_id}", json={"completed":True}, headers=headers)
    assert res.status_code == 200
    assert res.json()["completed"] == True

def test_unauthenticated_blocked():
    res = client.get("/tasks/")  # no token
    assert res.status_code == 401