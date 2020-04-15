import random
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    num = random.randint(0, 10000)
    return render_template("index.html", name="Jimmy", num=num)

@app.route("/goodbye")
def bye():
    return "Goodbye."