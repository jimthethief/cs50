import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, compare

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # query finance.db sales table for results of purchases for current user grouped by stock symbol (exc. shares that have been sold: having cost > 0)
    # tracker table determines number of shares user currently holds
    session["getStocks"] = db.execute("SELECT sales.user_id, sales.symbol, sales.name, SUM(cost) AS holdings, tracker.shares, ROUND((SUM(cost) / tracker.shares), 2) AS value FROM sales JOIN tracker ON sales.symbol=tracker.symbol WHERE sales.user_id = :user AND tracker.user_id = :user GROUP BY sales.symbol HAVING tracker.shares > 0;",
                                      user=session["user_id"])

    # get cash balance of current user
    getBalance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # # iterate through rows to determine total value of shares
    # session["overall"] stores total current price of all shares (using lookup())
    session["overall"] = 0
    # session["lossGain"] stores total price of all shares when purchased (using holdings column)
    session["lossGain"] = 0
    for stock in session["getStocks"]:
        session["overall"] += stock["shares"] * (lookup(stock["symbol"])["price"])
        session["lossGain"] += stock["holdings"]

    # current cash balance of user
    session["balance"] = getBalance[0]["cash"]
    # current value of shares + cash balance
    session["overall"] += session["balance"]
    # purchased value of shares + cash balance
    session["lossGain"] += session["balance"]
    # check if user has made overall losses or gains and return html element using compare helper
    session["ovrArrow"] = compare(session["overall"], session["lossGain"])

    # push required variables and helpers to index.html
    return render_template('index.html',
                           getStocks=session["getStocks"],
                           balance=session["balance"],
                           overall=session["overall"],
                           ovrArrow=session["ovrArrow"],
                           lookup=lookup,
                           float=float,
                           usd=usd,
                           compare=compare)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    else:
        # save lookup request in session variable
        session["result"] = lookup(request.form.get("symbol"))
        session["amount"] = request.form.get("shares")

        # if lookup doesn't return result, fire error message and reload page
        if not session["result"]:
            flash("Sorry, that symbol isn't valid — try again.", 'alert-warning')
            return redirect('/buy')

        # if lookup returns dict of key value pairs, store those values in variables
        session["name"] = session["result"]["name"]
        session["price"] = float(session["result"]["price"])
        session["symbol"] = session["result"]["symbol"]
        session["shares"] = int(session["amount"])
        session["total"] = session["price"] * session["shares"]

        getUser = db.execute("SELECT * FROM users WHERE id = ?",
                             session["user_id"])

        # check that user has enough funds for purchase
        if (session["total"] > getUser[0]["cash"]):
            flash("Sorry, insufficient funds to carry out that transaction.", 'alert-danger')
            return redirect('/buy')

        # if user has funds - add purchase details into sales table
        db.execute("INSERT INTO sales (user_id, symbol, name, price, shares, cost, time) VALUES (?, ?, ?, ?, ?, ?, datetime('now', 'localtime'));",
                   session["user_id"], session["symbol"], session["name"], session["price"], session["shares"], session["price"] * session["shares"])

        # replace values in tracker table where user already has stocks in that symbol, creates new row otherwise
        db.execute("REPLACE INTO tracker(stock_id, user_id, symbol, name, shares) VALUES(?, ?, ?, ?, ?)",
                   str(session["user_id"]) + session["symbol"], session["user_id"], session["symbol"], session["name"], session["shares"])

        # update user funds
        session["newBalance"] = (getUser[0]["cash"]) - session["total"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   session["newBalance"], session["user_id"])
        #  reload page and display success message confirming transaction
        flash('You successfully purchased ' + str(session["shares"]) + ' share(s) in ' + session["name"] + '. Your new balance is ' + str(usd(session["newBalance"])) + '.',
              'alert-success')
        return render_template('buy.html')

    return apology("Oops, something went awry", 403)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        session["getHistory"] = db.execute(
            "SELECT symbol, shares, price, cost, time FROM sales WHERE user_id=? ORDER BY time DESC;", session["user_id"])
        return render_template('history.html',
                               getHistory=session["getHistory"],
                               usd=usd)

    else:
        # save search request in session variable
        session["symbol"] = request.form.get("symbol").upper()
        session["getRecords"] = db.execute("SELECT symbol, shares, price, cost, time FROM sales WHERE user_id=? AND symbol=?;",
                                           session["user_id"], session["symbol"])

        # if table search doesn't return result, fire error message and reload page
        if len(session["getRecords"]) < 1:
            flash("Sorry, we couldn't find any results for that symbol — try again.", 'alert-warning')
            return redirect('/history')

        # if search returns result(s), deliver those values to results.html template
        return render_template('results.html',
                               getRecords=session["getRecords"],
                               usd=usd)

    return apology("Oops, something went awry", 403)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username").lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Your password and/or username were entered incorrectly.', 'alert-danger')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

    return apology("Oops, something went awry", 403)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        # save lookup request in session variable
        session["result"] = lookup(request.form.get("symbol"))

        # if lookup doesn't return result, fire error message and reload page
        if not session["result"]:
            flash("Sorry, that symbol isn't valid — try again.", 'alert-warning')
            return redirect('/quote')

        # if lookup returns dict of key value pairs, deliver those values to quoted.html template
        return render_template('quoted.html',
                               name=session["result"]["name"],
                               price=usd(session["result"]["price"]),
                               symbol=session["result"]["symbol"])

    return apology("Oops, something went awry", 403)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # check username is valid (has been entered and isn't already in database)
        username = request.form.get("username").lower()
        if not username or db.execute("SELECT * FROM users WHERE username = ?", username):
            flash('Username is invalid or already in use.', 'alert-danger')
            return redirect("/register")

        # check that password & confirmation have been entered and that they match
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation or password != confirmation:
            flash('Password is invalid or passwords do not match.', 'alert-danger')
            return redirect("/register")

        # hash password and save user to database
        phash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, phash)

        # locate and remember new user
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash('Your sign-up was successful. Welcome aboard!', 'alert-success')
        return redirect("/")

    return apology("Oops, something went awry", 403)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        session["getStocks"] = db.execute("SELECT symbol, name, shares FROM tracker where user_id = ? GROUP BY symbol HAVING shares > 0;",
                                          session["user_id"])
        return render_template("sell.html",
                               getStocks=session["getStocks"])

    else:

        # save lookup request in session variable
        session["result"] = lookup(request.form.get("symbol"))
        session["shares"] = int(request.form.get("shares"))

        # if lookup doesn't return result, fire error message and reload page
        if not session["result"]:
            flash("Sorry, that symbol isn't valid — try again.", 'alert-warning')
            return redirect('/sell')

        # if lookup returns dict of key value pairs, store those values in variables
        session["symbol"] = session["result"]["symbol"]
        session["name"] = session["result"]["name"]
        session["price"] = float(session["result"]["price"])
        session["total"] = session["price"] * session["shares"]

        session["checkCash"] = db.execute("SELECT cash FROM users WHERE id = ?",
                                          session["user_id"])
        session["checkStocks"] = db.execute("SELECT shares FROM tracker WHERE user_id = ? AND symbol = ?",
                                            session["user_id"], session["symbol"])

        if session["shares"] > session["checkStocks"][0]["shares"]:
            flash("Sorry, insufficient shares to carry out that transaction.", 'alert-danger')
            return redirect('/sell')

        session["newBalance"] = session["checkCash"][0]["cash"] + session["total"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   session["newBalance"], session["user_id"])

        db.execute("UPDATE tracker SET shares = shares - ? WHERE user_id = ? AND symbol = ?",
                   session["shares"], session["user_id"], session["symbol"])

        # if user has funds - add purchase details into transaction table
        db.execute("INSERT INTO sales (user_id, symbol, name, price, shares, cost, time) VALUES (?, ?, ?, ?, ?, ?, datetime('now', 'localtime'));",
                   session["user_id"], session["symbol"], session["name"], -abs(session["price"]), session["shares"], -abs(session["price"]) * session["shares"])

        #  reload page and display success message confirming transaction
        flash('You successfully sold ' + str(session["shares"]) + ' share(s) in ' + session["name"] + '. Your new balance is ' + str(usd(session["newBalance"])) + '.',
              'alert-success')
        return redirect('/sell')

    return apology("Oops, something went awry", 403)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
