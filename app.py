# BudgetBuddy main application file

from flask import Flask, request, jsonify
from db.crud import create_user, get_users
from db.database import init_db


app = Flask(__name__)


# initialize databse tables
init_db()


# home
@app.route("/")
def home():
    return "BudgetBuddy backend is running! :)"


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