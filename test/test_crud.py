import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
import db.crud as crud

from datetime import date


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    # init
    Base.metadata.create_all(engine)

    # override SessionLocal in crud
    monkeypatch.setattr(crud, "SessionLocal", TestingSessionLocal)

    crud.pre_categories()

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


def test_create_transaction_success():
    # Create Category for transaction test 
    success, category = crud.create_category("Food")
    assert success is True
    assert category.name == "Food"

    cat_id = category.category_id

    success, transaction = crud.create_transaction(
        user_id=1,
        amount=100,
        category_id=cat_id,
        date=date(2024, 1, 1),
        description="Lunch"
    )

    assert success is True
    assert transaction.amount == 100
    assert transaction.category_id == cat_id


# Non exsisting category
def test_create_transaction_invalid_category():
    success, msg = crud.create_transaction(
        user_id = 1,
        amount = 50,
        category_id = 999,  
        date=date(2024, 1, 1),
        description = "Invalid category test"
    )

    assert success is False


def test_update_password_success():
    crud.create_user("pw@test.com", "A", "B", "pwuser", "oldpassword")

    success, user = crud.update_password("pw@test.com", "newpassword")

    assert success is True
    assert user.password == "newpassword"


def test_update_password_user_not_found():
    success, msg = crud.update_password("nonexistent@test.com", "newpassword")

    assert success is False
    assert msg == "No account with that email"


def test_get_user_by_email():
    crud.create_user("gresa@test.com", "Gresa", "Hoxha", "gresah", "mypassword")
    user = crud.get_user_by_email("gresa@test.com")

    assert user is not None
    assert user.username == "gresah"
    assert user.password == "mypassword"


def test_get_users():
    crud.create_user("messi@goat.com", "Lionel", "Messi", "Messiah", "goal")
    crud.create_user("ronaldinho@goat.com", "Ronaldo", "Moreira", "Ronaldinho", "smile")
    users = crud.get_users()
    assert len(users) == 2
    assert users[0].username == "Messiah"
    assert users[1].password == "smile"

def test_get_balance():

    crud.add_income(user_id=1, amount=25000, category_id=1, date=date(2024, 1, 1))
    crud.add_expense(user_id=1, amount=500, category_id=2, date=date(2024, 1, 2))

    balance = crud.get_balance(1, year=2024, month =1)

    assert balance == 24500


def test_delete_user_success():
    crud.create_user("del@test.com", "A", "B", "deluser", "pass")
    success, msg = crud.delete_user("del@test.com", "pass")
    assert success is True
    assert crud.get_user_by_email("del@test.com") is None


def test_delete_user_failures():
    crud.create_user("del2@test.com", "A", "B", "deluser2", "pass")
    success, msg = crud.delete_user("del2@test.com", "wrongpass") ## test for wrong passoword
    assert msg == "Wrong password" 
    success, msg = crud.delete_user("none@test.com", "pass") ##test if no user with that email exist
    assert msg == "No account with that email"


def test_get_transactions():
    crud.create_transaction(user_id=1, amount=100, category_id=1, date=date(2024, 1, 1))
    crud.create_transaction(user_id=1, amount=200, category_id=2, date=date(2024, 1, 2))
    transactions = crud.get_transaction(1, year =2024, month = 1)
    assert len(transactions) == 2


def test_get_category():
    categories = crud.get_category()
    assert len(categories) == 5
    assert categories[0].name == "Salary"

def test_update_goal_success():
    crud.create_user("goal@test.com", "A", "B", "goaluser", "pass")
    success, user = crud.update_goal("goal@test.com", 5000)
    assert success is True
    assert user.goal == 5000


def test_update_goal_set_none():
    crud.create_user("goal2@test.com", "A", "B", "goaluser2", "pass")
    crud.update_goal("goal2@test.com", 5000)
    success, user = crud.update_goal("goal2@test.com", None)
    assert success is True
    assert user.goal is None


def test_update_goal_user_not_found():
    success, msg = crud.update_goal("nonexistent@test.com", 5000)
    assert success is False
    assert msg == "No account with that email"
