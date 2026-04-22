# BudgetBuddy main application file
# Hello from main
# Hello from database
# Jaha men hallå där från frontend också

import time
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from db.crud import create_user, get_users, get_user_by_email
from flask import Flask
from db.database import init_db

app = Flask(__name__)
app.secret_key = "super-secret-key"

# 5 minutes timeout
SESSION_TIMEOUT = 300

# initialize database tables
init_db()


# home is login page
# Initialize database
init_db()

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
    
    return render_template("dashboard.html")


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


if __name__ == "__main__":
    app.run(debug=True)