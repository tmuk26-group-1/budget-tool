# BudgetBuddy main application file
# Hello from main
# Hello from database
# Jaha men hallå där från frontend också

import time
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from db.crud import create_user, get_users, get_user_by_email, get_balance, get_category, add_income, add_expense
from db.database import init_db

app = Flask(__name__)
app.secret_key = "super-secret-key"

# 5 minutes timeout
SESSION_TIMEOUT = 300

init_db()

# home is login page

##home
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = get_user_by_email(email)

    if user and user.password == password:
        # Successful login
        session["user_id"] = user.user_id
        session["login_time"] = time.time()
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

    # Call CRUD function
    success, result = create_user(email, firstname, lastname, username, password)

    if success:
        # On success, redirect to login page
        return redirect(url_for("home"))
    else:
        # on failure, show registration page again with error message
        return render_template("registration.html", error=result)


# users
@app.route("/users", methods=["GET"])
def users():
    users = get_users()
    return jsonify([{
        "id": u.id,
        "email": u.email,
        "firstname": u.firstname,
        "lastname": u.lastname,
        "username": u.username
    } for u in users])


# dashboard
@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    login_time = session.get("login_time")

    # Not logged in
    if not user_id or not login_time:
        return redirect (url_for("home"))
    
    if time.time() - login_time > SESSION_TIMEOUT:
        session.clear()
        return redirect (url_for("home"))
    
    balance = get_balance(user_id)
    return render_template("dashboard.html", balance=balance)


#GET route for adding transaction
@app.route("/add_transaction", methods=["GET"])
def add_transaction():
    user_id = session.get("user_id")
    login_time = session.get("login_time")

    if not user_id or not login_time:
        return redirect(url_for("home"))
    
    if time.time() - login_time > SESSION_TIMEOUT:
        session.clear()
        return redirect(url_for("home"))
    
    #Fetch categories for dropdown
    categories = get_category()
    return render_template("add_transaction.html", categories=categories)

#POST route for adding transaction
@app.route("/add_transaction", methods=["POST"])
def add_transaction_post():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("home"))

    amount = request.form.get("amount")
    category_id = request.form.get("category_id")
    transaction_type = request.form.get("type")

    # Basic validation
    if not amount or not category_id or not transaction_type:
        categories = get_category()
        return render_template(
            "add_transaction.html",
            categories=categories,
            error="All fields are required."
        )

    amount = float(amount)
    import datetime
    date = datetime.date.today()

    if transaction_type == "income":
        success, result = add_income(user_id, amount, category_id, date)
    else:  # "expense"
        success, result = add_expense(user_id, amount, category_id, date)

    if success:
        return redirect(url_for("dashboard"))
    else:
        categories = get_category()
        return render_template(
            "add_transaction.html",
            categories=categories,
            error=result
        )



if __name__ == "__main__":
    app.run(debug=True)