# BudgetBuddy main application file
# Hello from database

from flask import Flask
from db.database import init_db

app = Flask(__name__)

# Initialize database
init_db()

##home
@app.route("/")
def home():
    return "BudgetBuddy backend is running! :)"

if __name__ == "__main__":
    app.run(debug=True)