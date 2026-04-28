import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from db.database import Base
import db.crud as crud


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture
def client(monkeypatch):
    # Create tables
    Base.metadata.create_all(engine)

    # Patch SessionLocal in crud
    monkeypatch.setattr(crud, "SessionLocal", TestingSessionLocal)

    crud.pre_categories()

    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"

    with app.test_client() as client:
        yield client

    Base.metadata.drop_all(engine)


def test_login_and_access_dashboard(client):
    # Arrange: create user in DB
    success, user = crud.create_user(
        "test@test.com",
        "Test",
        "User",
        "testuser",
        "password"
    )
    assert success is True

    # Act: login via route
    response = client.post(
        "/login",
        data={
            "email": "test@test.com",
            "password": "password"
        },
        follow_redirects=False
    )

    # Assert: redirect to dashboard
    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]

    # Follow redirect
    dashboard_response = client.get("/dashboard")
    assert dashboard_response.status_code == 200
    assert b"Remaining Budget" in dashboard_response.data