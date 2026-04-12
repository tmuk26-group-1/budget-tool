# BudgetBuddy main application file
# Hello from main
# Hello from database

import time
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from db.crud import create_user, get_users
from db.database import init_db

app = Flask(__name__)
app.secret_key = "super-secret-key"

# 5 minutes timeout
SESSION_TIMEOUT = 300

# Initialize database
init_db()

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.before_request
def check_session_timeout():
    protected_routes = ["dashboard"]

    if request.endpoint in protected_routes:
        user_id = session.get("user_id")
        login_time = session.get("login_time")

        # Inte inloggad
        if not user_id or not login_time:
            session.clear()
            return redirect(url_for("home"))

        # Session gått ut
        if time.time() - login_time > SESSION_TIMEOUT:
            session.clear()
            return redirect(url_for("home"))

        # Förläng session vid aktivitet (sliding timeout)
        session["login_time"] = time.time()

# home is login page

##home
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    print("Recieved login:", email, password)
    
    # simulate a logged in user
    session["user_id"] = 1
    session["login_time"] = time.time() 

    return redirect (url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# register
@app.route("/register", methods=["POST"])
def register():
    data = request.json     # froentend must send JSON
    
    email = data.get("email")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    username = data.get("username")
    password = data.get("password")

    # Call CRUD function
    create_user(email, firstname, lastname, username, password)

    return jsonify({"message": "User created succesfully"}), 201


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