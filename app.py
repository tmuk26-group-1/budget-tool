# BudgetBuddy main application file

from flask import Flask

app = Flask(__name__)

##home
@app.route("/")
def home():
    return "BudgetBuddy backend is running! :)"

if __name__ == "__main__":
    app.run(debug=True)