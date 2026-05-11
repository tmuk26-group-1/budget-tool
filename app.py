# BudgetBuddy main application file
# Hello from main
# Hello from database
# Jaha men hallå där från frontend också

import time
import logging
from functools import wraps
from datetime import datetime

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from db.crud import (
    create_user,
    get_users,
    get_user_by_email,
    get_balance,
    get_category,
    add_income,
    add_expense,
    get_user_by_id,
    update_goal,
    get_total_savings,
    add_savings,
    withdraw_savings,
    get_transaction,
    get_category_totals,
)
from db.database import init_db

app = Flask(__name__)
app.secret_key = "super-secret-key"

# 5 minutes timeout
SESSION_TIMEOUT = 300

# Basic logging
logging.basicConfig(level=logging.INFO)

init_db()


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return wrapper


def check_timeout():
    """Return False if session is missing or expired, True otherwise."""
    login_time = session.get("login_time")
    if not login_time:
        return False
    if time.time() - login_time > SESSION_TIMEOUT:
        logging.info("Session timeout, clearing session")
        session.clear()
        return False
    return True


def next_month(year, month):
    if month == 12:
        return year + 1, 1
    return year, month + 1


def prev_month(year, month):
    if month == 1:
        return year - 1, 12
    return year, month - 1


def format_transaction(t):
    """Helper to format a Transaction object for display."""
    return {
        "amount": f"{t.amount} kr",
        "is_positive": t.amount > 0,
        "date": t.date.strftime("%d/%m"),
        "desc": t.description or "",
    }


# home is login page

##home
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = get_user_by_email(email)

    if user and check_password_hash(user.password, password):
        # Successful login
        session["user_id"] = user.user_id
        session["login_time"] = time.time()
        logging.info(f"User {user.user_id} logged in")
        return redirect(url_for("dashboard"))
    else:
        # Failed login
        return render_template("login.html", error="Invalid email or password")


@app.route("/register", methods=["GET"])
def register_get():
    return render_template("registration.html")


@app.route("/forgot-password", methods=["GET"])
def forgot_password():
    return render_template("forgot-password.html")


@app.route("/check-email", methods=["POST"])
def check_email():
    data = request.get_json()
    email = data.get("email")

    from db.crud import get_users
    users = get_users()
    exists = any(u.email == email for u in users)

    return jsonify({"exists": exists})


@app.route("/reset-password", methods=["POST"])
def reset_password():
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if new_password != confirm_password:
        return render_template("forgot-password.html", error="Passwords do not match")

    from db.crud import update_password
    success, result = update_password(email, new_password)

    if success:
        return redirect(url_for("home"))
    else:
        return render_template("forgot-password.html", error=result)


# register
@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    username = request.form.get("username")
    password = request.form.get("password")

    # Hash password
    hashed_password = generate_password_hash(password)
    # Call CRUD function
    success, result = create_user(
        email,
        firstname,
        lastname,
        username,
        hashed_password,
    )

    if success:
        # On success, redirect to login page
        logging.info(f"New user registered: {email}")
        return redirect(url_for("home"))
    else:
        # on failure, show registration page again with error message
        return render_template("registration.html", error=result)


# users
@app.route("/users", methods=["GET"])
def users():
    users = get_users()
    return jsonify([
        {
            "id": u.user_id,
            "email": u.email,
            "firstname": u.firstname,
            "lastname": u.lastname,
            "username": u.username,
        }
        for u in users
    ])


# dashboard
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_id = session.get("user_id")

    if not check_timeout():
        return redirect(url_for("home"))

    # Always load user first
    user = get_user_by_id(user_id)

    # Handle monthly goal update
    if request.method == "POST":
        new_goal = int(request.form.get("monthly_goal"))
        update_goal(user.email, new_goal)

        # Refresh user AFTER updating goal
        user = get_user_by_id(user_id)

    # Get current year and month (with query override)
    now = datetime.now()
    year = request.args.get("year", now.year, type=int)
    month = request.args.get("month", now.month, type=int)

    username = user.username

    prev_y, prev_m = prev_month(year, month)
    next_y, next_m = next_month(year, month)

    # Core dashboard values
    balance = get_balance(user_id, year, month)
    monthly_goal = int(user.goal or 0)

    # NEW: highlight goal when it exceeds remaining budget
    goal_exceeds_budget = monthly_goal > balance

    # Transactions
    transactions = get_transaction(user_id, year, month)
    formatted_transactions = [format_transaction(t) for t in transactions]

    # Category totals for chart
    category_totals = get_category_totals(user_id, year, month)
    chart_labels = list(category_totals.keys())
    chart_values = list(category_totals.values())

    # Savings
    _, total_savings = get_total_savings(user_id)
    savings_error = request.args.get("error")

    logging.info(f"User {user_id} opened dashboard for {month}/{year}")

    return render_template(
        "dashboard.html",
        balance=balance,
        username=username,
        year=year,
        month=month,
        prev_y=prev_y,
        prev_m=prev_m,
        next_y=next_y,
        next_m=next_m,
        monthly_goal=monthly_goal,
        goal_exceeds_budget=goal_exceeds_budget,
        total_savings=total_savings,
        savings_error=savings_error,
        transactions=formatted_transactions,
        chart_labels=chart_labels,
        chart_values=chart_values,
    )


# GET route for adding transaction
@app.route("/add_transaction", methods=["GET"])
@login_required
def add_transaction():
    if not check_timeout():
        return redirect(url_for("home"))

    # Fetch categories for dropdown
    categories = get_category()
    return render_template("add_transaction.html", categories=categories)


# POST route for adding transaction
@app.route("/add_transaction", methods=["POST"])
@login_required
def add_transaction_post():
    if not check_timeout():
        return redirect(url_for("home"))

    user_id = session.get("user_id")

    amount = request.form.get("amount")
    category_id = request.form.get("category_id")
    description = request.form.get("description")
    transaction_type = request.form.get("type")

    # Basic validation
    if not amount or not category_id or not transaction_type:
        categories = get_category()
        return render_template(
            "add_transaction.html",
            categories=categories,
            error="All fields are required.",
        )

    amount = float(amount)
    import datetime as dt
    date = dt.date.today()

    if transaction_type == "income":
        success, result = add_income(user_id, amount, category_id, date, description)
    else:  # "expense"
        success, result = add_expense(user_id, amount, category_id, date, description)

    if success:
        logging.info(f"User {user_id} added {transaction_type} of {amount}")
        return redirect(url_for("dashboard"))
    else:
        categories = get_category()
        return render_template(
            "add_transaction.html",
            categories=categories,
            error=result,
        )


# route for logout button
@app.route("/logout")
def logout():
    logging.info("User logged out")
    session.clear()  # removes user_id and login_time
    return redirect(url_for("home"))


@app.route("/update_savings", methods=["POST"])
@login_required
def update_savings_route():
    if not check_timeout():
        return redirect(url_for("home"))

    user_id = session.get("user_id")
    amount = request.form.get("amount")

    today = datetime.today()

    if not amount:
        return redirect(url_for("dashboard"))

    try:
        amount = int(amount)
    except ValueError:
        return redirect(url_for("dashboard"))

    action = request.form.get("action")
    if action == "withdraw":
        success, msg = withdraw_savings(user_id, amount, today)
    else:
        success, msg = add_savings(user_id, amount, today)

    if not success:
        return redirect(url_for("dashboard", error=msg))
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)