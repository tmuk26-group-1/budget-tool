import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
import db.crud as crud


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    # init
    Base.metadata.create_all(engine)

    # override SessionLocal in crud
    monkeypatch.setattr(crud, "SessionLocal", TestingSessionLocal)

    yield

    Base.metadata.drop_all(engine)


# --- TESTS --- #

def test_create_user_success():
    success, user = crud.create_user(
        "test@test.com",
        "Test",
        "User",
        "testuser",
        "password"
    )

    assert success is True
    assert user.email == "test@test.com"


def test_create_user_duplicate_email():
    crud.create_user("test@test.com", "A", "B", "user1", "pass")

    success, msg = crud.create_user(
        "test@test.com",
        "C",
        "D",
        "user2",
        "pass"
    )

    assert success is False
    assert msg == "Email already registered"


def test_create_user_duplicate_username():
    crud.create_user("a@test.com", "A", "B", "user1", "pass")

    success, msg = crud.create_user(
        "b@test.com",
        "C",
        "D",
        "user1",
        "pass"
    )

    assert success is False
    assert msg == "Username already taken"