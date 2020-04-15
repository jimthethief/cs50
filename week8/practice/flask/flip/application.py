import random
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    name = request.args.get("name")
    if not name:
        name = "stranger"
    return render_template("hello.html", name=name)

@app.route("/flip")
def flip():
    num = random.randint(0, 1)
    flip = request.args.get("flip")
    result = "Huh?"
    if flip == 'Heads' and num == 0 or flip == 'Tails' and num == 1:
        result = "You Win!"
    else:
        result = "You Lose!"
    return render_template("flip.html", num=num, flip=flip, result=result)