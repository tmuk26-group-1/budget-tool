# BudgetBuddy main application file

from flask import Flask, request, jsonify, render_template
from db.crud import create_user, get_users
from db.database import init_db
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask import Flask, request, jsonify, render_template, redirect, url_for, session



app = Flask(__name__)
app.secret_key = "super-secret-key"


# initialize database tables
init_db()

# dashboard
@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    return render_template("dashboard.html")


# home is login page
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

    return redirect (url_for("dashboard"))


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