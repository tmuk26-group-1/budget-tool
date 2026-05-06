import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from app import app, format_transaction
from db.database import Base
import db.crud as crud

from datetime import date


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


# ---------------------------------------------------------
# LOGIN / LOGOUT / SESSION TESTS
# ---------------------------------------------------------

def test_login_and_access_dashboard(client):
    success, user = crud.create_user(
        "test@test.com", "Test", "User", "testuser",
        generate_password_hash("password")
    )
    assert success

    response = client.post(
        "/login",
        data={"email": "test@test.com", "password": "password"},
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]

    dashboard_response = client.get("/dashboard")
    assert dashboard_response.status_code == 200
    assert b"Remaining Balance" in dashboard_response.data


def test_login_failure(client):
    response = client.post(
        "/login",
        data={"email": "wrong@test.com", "password": "nope"},
        follow_redirects=True
    )
    assert b"Invalid email or password" in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302


def test_session_timeout(client, monkeypatch):
    success, user = crud.create_user(
        "timeout@test.com", "A", "B", "timeoutuser",
        generate_password_hash("pass")
    )
    assert success

    client.post("/login", data={"email": "timeout@test.com", "password": "pass"})

    # Force session to be expired
    monkeypatch.setattr("time.time", lambda: 0)

    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302


def test_logout_clears_session(client):
    success, user = crud.create_user(
        "logout@test.com", "A", "B", "logoutuser",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "logout@test.com", "password": "pass"})

    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302

    dashboard = client.get("/dashboard", follow_redirects=False)
    assert dashboard.status_code == 302


# ---------------------------------------------------------
# ADD TRANSACTION TESTS
# ---------------------------------------------------------

def test_add_transaction_get(client):
    success, user = crud.create_user(
        "addget@test.com", "A", "B", "addgetuser",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "addget@test.com", "password": "pass"})

    response = client.get("/add_transaction")
    assert response.status_code == 200
    assert b"Add Transaction" in response.data


def test_add_transaction_post_success(client):
    success, user = crud.create_user(
        "addpost@test.com", "A", "B", "addpostuser",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "addpost@test.com", "password": "pass"})

    categories = crud.get_category()
    cat_id = categories[0].category_id

    response = client.post(
        "/add_transaction",
        data={"amount": "100", "category_id": cat_id, "type": "income"},
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]


def test_add_transaction_post_missing_fields(client):
    success, user = crud.create_user(
        "missing@test.com", "A", "B", "missinguser",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "missing@test.com", "password": "pass"})

    response = client.post(
        "/add_transaction",
        data={"amount": "", "category_id": "", "type": ""},
        follow_redirects=True
    )

    assert b"All fields are required" in response.data


def test_add_transaction_requires_login(client):
    response = client.get("/add_transaction", follow_redirects=False)
    assert response.status_code == 302


# ---------------------------------------------------------
# DASHBOARD TESTS
# ---------------------------------------------------------

def test_dashboard_month_navigation(client):
    success, user = crud.create_user(
        "month@test.com", "A", "B", "monthuser",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "month@test.com", "password": "pass"})

    response = client.get("/dashboard?year=2025&month=12")
    assert b"2025" in response.data
    assert b"12" in response.data


def test_prev_month_edge_case(client):
    success, user = crud.create_user(
        "edge@test.com", "A", "B", "edgeuser",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "edge@test.com", "password": "pass"})

    response = client.get("/dashboard?year=2025&month=1")
    assert response.status_code == 200


def test_next_month_normal_case(client):
    success, user = crud.create_user(
        "next@test.com", "A", "B", "nextuser",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "next@test.com", "password": "pass"})

    response = client.get("/dashboard?year=2025&month=3")
    assert response.status_code == 200


def test_dashboard_shows_username(client):
    success, user = crud.create_user(
        "name@test.com", "Test", "User", "testname",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "name@test.com", "password": "pass"})

    response = client.get("/dashboard")
    assert b"testname" in response.data


def test_dashboard_custom_month(client):
    crud.create_user(
        "custom@test.com", "A", "B", "customuser",
        generate_password_hash("pass")
    )
    client.post("/login", data={"email": "custom@test.com", "password": "pass"})

    response = client.get("/dashboard?year=2024&month=5")
    assert b"2024" in response.data
    assert b"5" in response.data


# ---------------------------------------------------------
# REGISTRATION TESTS
# ---------------------------------------------------------

def test_register_success(client):
    response = client.post(
        "/register",
        data={
            "email": "new@test.com",
            "firstname": "New",
            "lastname": "User",
            "username": "newuser",
            "password": "pass123"
        },
        follow_redirects=False
    )
    assert response.status_code == 302


def test_register_duplicate_email(client):
    crud.create_user(
        "dup@test.com", "A", "B", "dupuser",
        generate_password_hash("pass")
    )

    response = client.post(
        "/register",
        data={
            "email": "dup@test.com",
            "firstname": "X",
            "lastname": "Y",
            "username": "dupuser2",
            "password": "pass"
        },
        follow_redirects=True
    )

    assert b"error" in response.data or b"exists" in response.data


# ---------------------------------------------------------
# PASSWORD RESET TESTS
# ---------------------------------------------------------

def test_forgot_password_page(client):
    response = client.get("/forgot-password")
    assert response.status_code == 200


def test_reset_password_mismatch(client):
    response = client.post(
        "/reset-password",
        data={
            "email": "x@test.com",
            "new_password": "abc",
            "confirm_password": "xyz"
        },
        follow_redirects=True
    )
    assert b"Passwords do not match" in response.data


def test_reset_password_success(client):
    crud.create_user(
        "reset@test.com", "A", "B", "resetuser",
        generate_password_hash("oldpass")
    )

    response = client.post(
        "/reset-password",
        data={
            "email": "reset@test.com",
            "new_password": "newpass",
            "confirm_password": "newpass"
        },
        follow_redirects=False
    )

    assert response.status_code == 302


# ---------------------------------------------------------
# CHECK EMAIL TEST
# ---------------------------------------------------------

def test_check_email_route(client):
    crud.create_user(
        "exists@test.com", "A", "B", "existsuser",
        generate_password_hash("pass")
    )

    response = client.post("/check-email", json={"email": "exists@test.com"})
    assert response.json["exists"] is True

    response = client.post("/check-email", json={"email": "nope@test.com"})
    assert response.json["exists"] is False


# ---------------------------------------------------------
# USERS ENDPOINT
# ---------------------------------------------------------

def test_users_endpoint(client):
    crud.create_user(
        "list@test.com", "A", "B", "listuser",
        generate_password_hash("pass")
    )

    response = client.get("/users")
    assert response.status_code == 200
    assert b"list@test.com" in response.data


# ---------------------------------------------------------
# FORMAT TRANSACTION TEST
# ---------------------------------------------------------

def test_format_transaction_function():
    class Dummy:
        amount = 150
        description = "Test"
        from datetime import date
        date = date(2025, 4, 21)

    result = format_transaction(Dummy)

    assert result["amount"] == "150 kr"
    assert result["is_positive"] is True
    assert result["date"] == "21/04"
    assert result["desc"] == "Test"


# ---------------------------------------------------------
# DASHBOARD LOAD TEST
# ---------------------------------------------------------
def test_dashboard_loads(client):
    success, user = crud.create_user(
        "dash@test.com", "Dash", "User", "dashuser",
        generate_password_hash("password")
    )
    assert success

    client.post("/login", data={"email": "dash@test.com", "password": "password"})

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Remaining Balance" in response.data
    assert b"Monthly Budgetgoal" in response.data


# ---------------------------------------------------------
# UPDATE MONTHLY GOAL TEST
# ---------------------------------------------------------
def test_update_monthly_goal(client):
    success, user = crud.create_user(
        "goal@test.com", "Goal", "User", "goaluser",
        generate_password_hash("password")
    )
    assert success

    client.post("/login", data={"email": "goal@test.com", "password": "password"})

    response = client.post("/dashboard", data={"monthly_goal": "5000"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"5000 kr" in response.data


# ---------------------------------------------------------
# MONTHLY GOAL WARNING (RED) TEST
# ---------------------------------------------------------
def test_goal_turns_red_when_exceeds_budget(client):
    success, user = crud.create_user(
        "warn@test.com", "Warn", "User", "warnuser",
        generate_password_hash("password")
    )
    assert success

    client.post("/login", data={"email": "warn@test.com", "password": "password"})

    # Add income so balance = 2000
    crud.add_income(user.user_id, 2000, "Salary", "2026-05-01")

    # Set goal to 5000 (greater than balance)
    client.post("/dashboard", data={"monthly_goal": "5000"})

    response = client.get("/dashboard")

    # Check for the warning class
    assert b"warning" in response.data


# ---------------------------------------------------------
# DASHBOARD REQUIRES LOGIN TEST
# ---------------------------------------------------------
def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert b"Login" in response.data


# ---------------------------------------------------------
# SESSION TIMEOUT TEST
# ---------------------------------------------------------
def test_session_timeout_redirects(client, monkeypatch):
    success, user = crud.create_user(
        "timeout@test.com", "Time", "Out", "timeoutuser",
        generate_password_hash("password")
    )
    assert success

    client.post("/login", data={"email": "timeout@test.com", "password": "password"})

    # Force timeout
    monkeypatch.setattr("app.check_timeout", lambda: False)

    response = client.get("/dashboard", follow_redirects=True)

    assert b"Login" in response.data or b"Welcome" in response.data


# ---------------------------------------------------------
# MONTH NAVIGATION TEST
# ---------------------------------------------------------
def test_month_navigation(client):
    success, user = crud.create_user(
        "nav@test.com", "Nav", "User", "navuser",
        generate_password_hash("password")
    )
    assert success

    client.post("/login", data={"email": "nav@test.com", "password": "password"})

    response = client.get("/dashboard?year=2026&month=5")

    assert b"5/2026" in response.data
    assert b"&lt;" in response.data
    assert b"&gt;" in response.data



# ---------------------------------------------------------
# SAVINGS DISPLAY TEST
# ---------------------------------------------------------
def test_savings_display(client):
    success, user = crud.create_user(
        "save@test.com", "Save", "User", "saveuser",
        generate_password_hash("password")
    )
    assert success

    client.post("/login", data={"email": "save@test.com", "password": "password"})

    response = client.get("/dashboard")

    assert b"Total Savings" in response.data


## expenses shown in dashboard
def test_expense_shows_in_dashboard(client):
    success, user = crud.create_user("balance@test.com", "Balance", "User", "balanceuser", generate_password_hash("password"))
    assert success

    client.post("/login", data = {"email": "balance@test.com", "password": "password"})
    
    categories = crud.get_category()
    for c in categories:
        if c.name == "Food & Groceries":
            food_cat = c
            break

    crud.add_expense(user.user_id, 300, food_cat.category_id, date(2026, 5, 1))

    response = client.get("/dashboard?year=2026&month=5")

    assert b"-300 kr" in response.data 