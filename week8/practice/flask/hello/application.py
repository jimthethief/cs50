from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1 style='font-family: 'Courier New', Courier; background: blue; color: white;'>Hello, world!</h1>"

@app.route("/goodbye")
def bye():
    return "Goodbye."