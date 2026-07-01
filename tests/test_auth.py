import pytest
from fastapi.testclient import TestClient

from main import app
from database import SessionLocal, Base, engine
import models
from utils import hash_password


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    db.add(models.User(email="test@example.com", hashed_password=hash_password("secret123")))
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_login_accepts_json_body():
    response = client.post(
        "/login",
        json={"email": "test@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert "access_token" in payload


def test_protected_route_accepts_bearer_prefixed_token_value():
    login_response = client.post(
        "/login",
        json={"email": "test@example.com", "password": "secret123"},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/users/1",
        headers={"Authorization": f"Bearer Bearer {token}"},
    )

    assert response.status_code == 200
