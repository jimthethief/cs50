import randomiser
from datetime import date
from helpers import apology, login_required
from generator import generateClubAttributes, generateFixtures
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# configure app
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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///champgaffer.db")


@app.route("/")
@login_required
def office():
    """Manager Hub"""

    # query champgaffer.db for player attributes
    session["getPlayers"] = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.manager_id = :manager AND player_attr.club_id = 20;",
                            manager=session["id"])

    # query champgaffer.db for star defender
    starDef = db.execute("SELECT name, age, nationality, flag, value, MAX(ovr) FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.player_id IN (SELECT player_attr.player_id FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE pos = \'GK\' OR pos = \'DEF\') AND club_id = 20 AND manager_id = ?;", 
                         session["id"])

    # query champgaffer.db for star attacker
    starAtt = db.execute("SELECT name, age, nationality, flag, value, MAX(ovr) FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.player_id IN (SELECT player_attr.player_id FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE pos = \'MID\' OR pos = \'ATT\') AND club_id = 20 AND manager_id = ?;", 
                         session["id"])
                            
    # query champgaffer.db for manager attributes
    getManager = db.execute("SELECT managers.name, managers.age, managers.club_name, managers.board_confidence, managers.budget, managers.season, managers.matchday, club_attr.rank, club_attr.ovr, clubs.primary_colour, clubs.secondary_colour FROM managers JOIN club_attr ON managers.id = club_attr.manager_id JOIN clubs ON managers.club_id = clubs.club_id WHERE managers.id = ? AND club_attr.club_id = 20;", 
                            session['id'])

    # query champgaffer.db for fixtures
    session["getFixtures"] = db.execute("SELECT home, away FROM fixtures JOIN managers ON fixtures.manager_id = managers.id WHERE managers.id = ? AND fixtures.week >= managers.matchday AND home = managers.club_name OR away = managers.club_name LIMIT 10;",
                             session["id"])
    
    session['managerStats'] = {
        "managername": getManager[0]['name'],
        "managerage": getManager[0]['age'],
        "clubname": getManager[0]['club_name'],
        "confidence": getManager[0]['board_confidence'],
        "budget": getManager[0]['budget'],
        "clubrank": getManager[0]['rank'],
        "clubovr": getManager[0]['ovr'],
        "season": getManager[0]['season'],
        "primary": getManager[0]['primary_colour'],
        "secondary": getManager[0]['secondary_colour']
    }

    session['starDef'] = {
        "playername": starDef[0]['name'],
        "playerage": starDef[0]['age'],
        "nationality": starDef[0]['nationality'],
        "flag": starDef[0]['flag'],
        "value": "£" + str(starDef[0]['value']) + "M",
        "ovr": starDef[0]['MAX(ovr)']
    }

    session['starAtt'] = {
        "playername": starAtt[0]['name'],
        "playerage": starAtt[0]['age'],
        "nationality": starAtt[0]['nationality'],
        "flag": starAtt[0]['flag'],
        "value": "£" + str(starAtt[0]['value']) + "M",
        "ovr": starAtt[0]['MAX(ovr)']
    }

    email = str(session['managerStats']['managername'] + "@" + session['managerStats']['clubname'] + ".co.uk").lower().replace(" ", "")

    return render_template('index.html',
                           getPlayers=session['getPlayers'],
                           getFixtures=session['getFixtures'],
                           managerStats=session['managerStats'],
                           starAtt=session['starAtt'],
                           starDef=session['starDef'],
                           email=email)


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
        rows = db.execute("SELECT * FROM managers WHERE username = :username",
                          username=request.form.get("username").lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Your password and/or username were entered incorrectly.', 'alert-danger')
            return render_template("login.html")

        # Remember which user has logged in
        session["id"] = rows[0]["id"]

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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register manager"""
    if request.method == "GET":
        return render_template("signup.html")
    else:
        # check username is valid (has been entered and isn't already in database)
        username = request.form.get("username").lower()
        if not username or db.execute("SELECT * FROM managers WHERE username = ?", username):
            flash('Username is invalid or already in use.', 'alert-danger')
            return redirect("/signup")

        # check name has been entered
        name = request.form.get("fullname").capitalize()
        if not name:
            flash('Please enter a name for your manager.', 'alert-danger')
            return redirect("/signup")

        # Query db for username
        cur = db.execute("SELECT * FROM managers WHERE username = ?", username)

        # check club name is valid (has been entered and isn't already in database)
        clubname = request.form.get("clubname")
        if not clubname or db.execute("SELECT * FROM managers WHERE club_name = ?", clubname):
            flash('Club name is invalid or already in use.', 'alert-danger')
            return redirect("/signup")

        # check that password & confirmation have been entered and that they match
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation or password != confirmation:
            flash('Password is invalid or passwords do not match.', 'alert-danger')
            return redirect("/signup")

        # hash password and save user to database
        phash = generate_password_hash(password)
        db.execute("INSERT INTO managers (username, hash, name, club_id, club_name, year) VALUES (?, ?, ?, 20, ?, ?);", 
                   username, phash, name, clubname, date.today().year)

        # rember logged in user
        session["id"] = cur[0]["id"]
        session["clubname"] = cur[0]["club_name"]

        # initialize player attributes
        getPlayers = db.execute("SELECT * FROM players;")
        generatePlayerAttributes(session["id"], getPlayers)
        
        # initialize club attributes
        getClubs = db.execute("SELECT * FROM clubs;")
        generateClubAttributes(session["id"], getClubs)
        
        # generate season 1 fixtures using helper function
        generateFixtures(session["id"], session["club_name"], date.today().year)
        
        # Redirect user to home page
        flash('Your sign-up was successful. Welcome aboard!', 'alert-success')
        return redirect("/")

    return apology("Oops, something went awry", 403)

"""
@app.route("/playercard", methods=["POST"])
def player():

    return render_template("playercard.html")

@app.route("/player", methods=["POST"])
def player():
    # get player id to search db request.form.get
    # store player attr in data to push to player.html
    playerid = request.form.get("playerid") #start / end

    data = []
    for i in range(4):
        data.append(f"Attribute #{i}")

    return jsonify(data)
"""