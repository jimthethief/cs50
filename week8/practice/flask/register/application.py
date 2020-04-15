from cs50 import SQL
from flask import Flask, redirect, render_template, request
from flask_session import Session

app = Flask(__name__)

db = SQL("sqlite:///register.db")

@app.route("/")
def index():
    users = db.execute("SELECT * FROM registrants")
    return render_template("index.html", users=users)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        if not name:
            return render_template("apology.html", message="You didn't provide a name.")
        email = request.form.get("email")
        if not email:
            return render_template("apology.html", message="You didn't provide an email address.")
        db.execute("INSERT INTO registrants (name, email) VALUES (?, ?);", name, email)
        return redirect("/")