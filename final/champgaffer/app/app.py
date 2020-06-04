from datetime import date
from random import randint
from helpers import apology, login_required
from generator import generateClubAttributes, generateFixtures, gotNews
from randomiser import makePlayer, makeAttr
from match import matchSetup, simMatch
from cs50 import SQL
from flask import Flask, flash, jsonify, json, redirect, render_template, request, session
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

    # query champgaffer.db for news items and fixtures
    session["getEmails"] = db.execute("SELECT * FROM news WHERE manager_id = ? ORDER BY news_id DESC LIMIT 10;",
                                      session["id"])

    # query champgaffer.db for player attributes
    session["getPlayers"] = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.manager_id = :manager AND player_attr.club_id = 20 ORDER BY squad_num;",
                            manager=session["id"])

    # query champgaffer.db for star defender
    starDef = db.execute("SELECT name, age, nationality, flag, value, MAX(ovr) FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.player_id IN (SELECT player_attr.player_id FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE pos = \'GK\' OR pos = \'DEF\') AND club_id = 20 AND manager_id = ?;", 
                         session["id"])

    # query champgaffer.db for star attacker
    starAtt = db.execute("SELECT name, age, nationality, flag, value, MAX(ovr) FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.player_id IN (SELECT player_attr.player_id FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE pos = \'MID\' OR pos = \'ATT\') AND club_id = 20 AND manager_id = ?;", 
                         session["id"])
                            
    # query champgaffer.db for manager attributes
    getManager = db.execute("SELECT name, age, managers.club_name, board_confidence, budget, season, current_season, matchday, rank, ovr, primary_colour, secondary_colour FROM managers JOIN club_attr ON managers.id = club_attr.manager_id JOIN clubs ON managers.club_id = clubs.club_id WHERE managers.id = ? AND club_attr.club_id = 20; ", 
                            session['id'])

    # query champgaffer.db for fixtures
    session["getFixtures"] = db.execute("SELECT home, away FROM fixtures JOIN managers ON fixtures.manager_id = managers.id WHERE (managers.id = ? AND week >= matchday) AND (home = managers.club_name OR away = managers.club_name) LIMIT 10;",
                             session["id"])
    
    session['managerStats'] = {
        "managername": getManager[0]['name'],
        "managerage": getManager[0]['age'],
        "clubname": getManager[0]['club_name'],
        "confidence": getManager[0]['board_confidence'],
        "budget": getManager[0]['budget'],
        "clubrank": getManager[0]['rank'],
        "clubovr": getManager[0]['ovr'],
        "season": getManager[0]['current_season'] - getManager[0]['season'],
        "primary": getManager[0]['primary_colour'],
        "secondary": getManager[0]['secondary_colour']
    }

    session['starDef'] = {
        "playername": starDef[0]['name'],
        "playerage": starDef[0]['age'],
        "nationality": starDef[0]['nationality'],
        "flag": starDef[0]['flag'],
        "value": "£" + str(starDef[0]['value']) + "m",
        "ovr": starDef[0]['MAX(ovr)']
    }

    session['starAtt'] = {
        "playername": starAtt[0]['name'],
        "playerage": starAtt[0]['age'],
        "nationality": starAtt[0]['nationality'],
        "flag": starAtt[0]['flag'],
        "value": "£" + str(starAtt[0]['value']) + "m",
        "ovr": starAtt[0]['MAX(ovr)']
    }

    session['email'] = str(session['managerStats']['managername'] + "@" + session['managerStats']['clubname'] + ".co.uk").lower().replace(" ", "")

    return render_template('index.html',
                           getEmails=session['getEmails'],
                           getPlayers=session['getPlayers'],
                           getFixtures=session['getFixtures'],
                           managerStats=session['managerStats'],
                           starAtt=session['starAtt'],
                           starDef=session['starDef'],
                           email=session['email'])


@app.route("/transfers", methods=["GET", "POST"])
@login_required
def transfers():
    """Search and buy players"""

    session["getClubs"] = db.execute("SELECT club_name FROM clubs WHERE club_id != 20 ORDER BY club_id DESC;")
    session["funds"] = db.execute("SELECT budget FROM managers WHERE id = ?;",
                                  session["id"])[0]

    if request.method == "GET":
        session["getPlayers"] = db.execute("SELECT players.player_id, name, nationality, flag, players.pos, clubs.club_id, player_attr.manager_id, squad_num, age, speed, strength, technique, potential, handsomeness, player_attr.ovr, value, club_name, primary_colour, secondary_colour, club_attr.rank FROM players JOIN player_attr ON players.player_id = player_attr.player_id JOIN clubs on player_attr.club_id = clubs.club_id JOIN club_attr ON player_attr.club_id = club_attr.club_id WHERE player_attr.manager_id = ? AND clubs.club_id != 20 ORDER BY value DESC;", 
                                           session["id"])
        
        return render_template('transfers.html',
                               getPlayers=session["getPlayers"],
                               getClubs=session["getClubs"],
                               funds=session["funds"]['budget'])
    else:
        # save search request in session variable
        session["name_search"] = request.form.get("name_search")
        session["club_search"] = request.form.get("club_search")
        session["pos_search"] = request.form.get("pos_search")
        session["val_search"] = int(request.form.get("val_search"))
        if request.form.get("ovr_search") == "":
            session["ovr_search"] = 1
        else:
            session["ovr_search"] = int(request.form.get("ovr_search"))

        
        session["getPlayers"] = db.execute("SELECT players.player_id, name, nationality, flag, players.pos, clubs.club_id, player_attr.manager_id, squad_num, age, speed, strength, technique, potential, handsomeness, player_attr.ovr, value, club_name, primary_colour, secondary_colour, club_attr.rank FROM players JOIN player_attr ON players.player_id = player_attr.player_id JOIN clubs on player_attr.club_id = clubs.club_id JOIN club_attr ON player_attr.club_id = club_attr.club_id WHERE player_attr.manager_id = :user AND name LIKE :name AND club_name LIKE :club AND players.pos LIKE :pos AND player_attr.ovr >= :ovr AND value <= :val AND clubs.club_id != 20 ORDER BY value DESC;",
                                           user=session["id"], name=('%{}%'.format(session['name_search']),), 
                                           club=('%{}%'.format(session['club_search']),), pos=('%{}%'.format(session['pos_search']),), 
                                           ovr=session['ovr_search'], val=session['val_search'])

        # if table search doesn't return result, fire error message and reload page
        if len(session["getPlayers"]) < 1:
            flash(f"Sorry, we couldn't find any matching results.", 'alert-warning')
            return redirect('/transfers')

        # if search returns result(s), deliver those values to results.html template
        return render_template('transfers.html',
                               getPlayers=session["getPlayers"],
                               getClubs=session['getClubs'],
                               funds=session["funds"]['budget'])
    
    return apology("Oops, something went awry", 403)


@app.route("/matchday", methods=["GET", "POST"])
@login_required
def matchday():
    """Select line-up/formation and show opposition"""
    if request.method == "GET":
        session["squad"] = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.manager_id = ? AND player_attr.club_id = 20 ORDER BY squad_num;",
                                    session["id"])

        session["fixture"] = db.execute("SELECT fixture_id, week, home, away, played FROM fixtures JOIN managers ON fixtures.manager_id = managers.id WHERE (managers.id = ? AND week = matchday) AND (home = managers.club_name OR away = managers.club_name);",
                                        session["id"])[0]

        if session["fixture"]["home"] == session["clubname"]:
            session["opponent"] = session["fixture"]["away"]
        else:
            session["opponent"] = session["fixture"]["home"]
        
        session["getOpponent"] = db.execute("SELECT club_name, primary_colour, secondary_colour, attendance, capacity, ovr, formation, pts, pos, rival, clubs.club_id FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE clubs.club_name = ? AND manager_id = ?;",
                                            session["opponent"], session["id"])[0]

        session["opponentSquad"] = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.manager_id = ? AND player_attr.club_id = ? ORDER BY squad_num;",
                                            session["id"], session["getOpponent"]["club_id"])

        return render_template('matchday.html',
                                squad=session["squad"],
                                squadSize=len(session["squad"]),
                                clubName=session["clubname"],
                                opponent=session["getOpponent"],
                                opponentSquad=session["opponentSquad"],
                                oppSquadSize=len(session["opponentSquad"]))
    else:
        
        return redirect("/match")


@app.route("/match", methods=["GET", "POST"])
@login_required
def match():
    """Simulate match"""
    if request.method == "POST":
        if session['fixture']['played'] == 0:
            session["userClub"] = db.execute("SELECT * FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE manager_id = ? AND clubs.club_id = 20;",
                                            session["id"])[0]

            if session["fixture"]["home"] == session["clubname"]:
                session["userSquad"] = json.loads(request.form.get("selection"))
                session['homeName'] = session["clubname"]
                session['awayName'] = session["getOpponent"]["club_name"]
                homeLineup = session["userSquad"][:11]
                awayLineup = session["opponentSquad"][:11]
                homeFormation = request.form.get("shape")
                awayFormation = session["getOpponent"]["formation"]
                homeInfo = session["userClub"]
                awayInfo = session["getOpponent"]
            else:
                session["userSquad"] = json.loads(request.form.get("selection"))
                session['homeName'] = session["getOpponent"]["club_name"]
                session['awayName'] = session["clubname"]
                homeLineup = session["opponentSquad"][:11]
                awayLineup = session["userSquad"][:11]
                homeFormation = session["getOpponent"]["formation"]
                awayFormation = request.form.get("shape")
                homeInfo = session["getOpponent"]
                awayInfo = session["userClub"]
            
            squadnum = 1
            for player in session["userSquad"]:
                db.execute("UPDATE player_attr SET squad_num = ? WHERE player_id = ? AND manager_id = ?;",
                squadnum, player["player_id"], session['id'])
                squadnum += 1

            session['home'], homeTeamList = matchSetup(homeLineup, homeFormation, homeInfo)
            session['away'], awayTeamList = matchSetup(awayLineup, awayFormation, awayInfo)
            session['homeGls'], session['awayGls'], session['homeScorers'], session['awayScorers'], session['attendance'] = simMatch(session['home'], homeTeamList, session['away'], awayTeamList)

            if session['homeGls'] > session['awayGls']:
                homePts = 3
                awayPts = 0
            elif session['awayGls'] > session['homeGls']:
                homePts = 0
                awayPts = 3
            else:
                homePts = 1
                awayPts = 1

            db.execute("UPDATE club_attr SET pld = :pld, gs = :gs, ga = :ga, pts = :pts WHERE manager_id = :id AND club_id = :club_id",
                        pld=session['fixture']['week'], gs=session['homeGls'], ga=session['awayGls'], pts=homeInfo['pts'] + homePts, id=session['id'], club_id=homeInfo['club_id'])
            
            db.execute("UPDATE club_attr SET pld = :pld, gs = :gs, ga = :ga, pts = :pts WHERE manager_id = :id AND club_id = :club_id",
                        pld=session['fixture']['week'], gs=session['awayGls'], ga=session['homeGls'], pts=awayInfo['pts'] + awayPts, id=session['id'], club_id=awayInfo['club_id'])

            session['fixture']['played'] = 1

            db.execute("UPDATE fixtures SET played = :played WHERE fixture_id = :fixture_id AND manager_id = :manager_id",
                        played=session['fixture']['played'], fixture_id=session['fixture']['fixture_id'], manager_id=session['id'])
            
            for scorer in session['homeScorers'] + session['awayScorers']:
                db.execute("INSERT INTO goals(manager_id, player_id, week, season) VALUES(:manager_id, :player_id, :week, :season)",
                            manager_id=session['id'], player_id=scorer['player_id'], week=session['fixture']['week'], season=session['managerStats']['season'])

            return render_template('match.html',
                                homeName=session['homeName'],
                                awayName=session['awayName'],
                                attendance=session["attendance"],
                                homeGls=session["homeGls"],
                                awayGls=session["awayGls"],
                                homeScorers=session['homeScorers'],
                                awayScorers=session['awayScorers'])
        else:
            return redirect("/results")
    else:
        return redirect("/matchday")

@app.route("/results", methods=["GET"])
@login_required
def results():
    """Simulate non-user matches"""
    session['getResults'] =  db.execute("SELECT fixture_id, week, home, away, played FROM fixtures JOIN managers ON fixtures.manager_id = managers.id WHERE (managers.id = ? AND week = matchday) AND (home != managers.club_name AND away != managers.club_name);",
                                        session["id"])
    
    if all(fixture['played'] == 0 for fixture in session['getResults']):                 
        session['topLeagueResults'] = []
        session['subLeagueResults'] = []
        
        userResult = {'home': session['homeName'], 'away': session['awayName'], 'homeGls': session['homeGls'], 'awayGls': session['awayGls'], 'homeScorers': session['homeScorers'], 'awayScorers': session['awayScorers']}
        
        if session["userClub"]['pos'] <= 10:
            session['topLeagueResults'].append(userResult)
        else:
            session['subLeagueResults'].append(userResult)

        for fixture in session['getResults']:
            homeSimName = fixture['home']
            awaySimName = fixture['away']
            homeSimInfo = db.execute("SELECT club_name, primary_colour, secondary_colour, attendance, capacity, ovr, formation, pos, gs, ga, pts, rival, clubs.club_id FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE clubs.club_name = ? AND manager_id = ?;",
                                    homeSimName, session["id"])[0]

            homeSimTeam = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.manager_id = ? AND player_attr.club_id = ?;",
                                    session["id"], homeSimInfo["club_id"])[:11]

            awaySimInfo = db.execute("SELECT club_name, primary_colour, secondary_colour, attendance, capacity, ovr, formation, pos, gs, ga, pts, rival, clubs.club_id FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE clubs.club_name = ? AND manager_id = ?;",
                                    awaySimName, session["id"])[0]

            awaySimTeam = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.manager_id = ? AND player_attr.club_id = ?;",
                                    session["id"], awaySimInfo["club_id"])[:11]
            
            homeSimFormation = homeSimInfo['formation']
            awaySimFormation = awaySimInfo['formation']

            homeSim, homeSimTeamList = matchSetup(homeSimTeam, homeSimFormation, homeSimInfo)
            awaySim, awaySimTeamList = matchSetup(awaySimTeam, awaySimFormation, awaySimInfo)
            homeSimGls, awaySimGls, homeSimScorers, awaySimScorers, simAttendance = simMatch(homeSim, homeSimTeamList, awaySim, awaySimTeamList)
            
            if homeSimGls > awaySimGls:
                homeSimPts = 3
                awaySimPts = 0
            elif awaySimGls > homeSimGls:
                homeSimPts = 0
                awaySimPts = 3
            else:
                homeSimPts = 1
                awaySimPts = 1
            
            if homeSimInfo['pos'] <= 10:
                session['topLeagueResults'].append({'home': homeSimName, 'away': awaySimName, 'homeGls': homeSimGls, 'awayGls': awaySimGls, 'homeScorers': homeSimScorers, 'awayScorers': awaySimScorers})
            else:
                session['subLeagueResults'].append({'home': homeSimName, 'away': awaySimName, 'homeGls': homeSimGls, 'awayGls': awaySimGls, 'homeScorers': homeSimScorers, 'awayScorers': awaySimScorers})
            
            db.execute("UPDATE club_attr SET pld = :pld, gs = :gs, ga = :ga, pts = :pts WHERE manager_id = :id AND club_id = :club_id",
                        pld=session['fixture']['week'], gs=homeSimInfo['gs'] + homeSimGls, ga=homeSimInfo['ga'] + awaySimGls, pts=homeSimInfo['pts'] + homeSimPts, id=session['id'], club_id=homeSimInfo['club_id'])
            
            db.execute("UPDATE club_attr SET pld = :pld, gs = :gs, ga = :ga, pts = :pts WHERE manager_id = :id AND club_id = :club_id",
                        pld=session['fixture']['week'], gs=awaySimInfo['gs'] + awaySimGls, ga=awaySimInfo['ga'] + homeSimGls, pts=awaySimInfo['pts'] + awaySimPts, id=session['id'], club_id=awaySimInfo['club_id'])

            fixture['played'] = 1
            session['matchday'] = session['fixture']['week'] + 1

            db.execute("UPDATE fixtures SET played = :played WHERE fixture_id = :fixture_id AND manager_id = :manager_id",
                        played=fixture['played'], fixture_id=fixture['fixture_id'], manager_id=session['id'])

            for scorer in homeSimScorers + awaySimScorers:
                db.execute("INSERT INTO goals(manager_id, player_id, week, season) VALUES(:manager_id, :player_id, :week, :season)",
                            manager_id=session['id'], player_id=scorer['player_id'], week=session['fixture']['week'], season=session['managerStats']['season'])

            db.execute("UPDATE managers SET matchday = ? WHERE id = ?",
                        session['matchday'], session["id"])

    return render_template('results.html',
                            topLeagueResults=session['topLeagueResults'],
                            subLeagueResults=session['subLeagueResults'])
   

@app.route("/teletable", methods=["GET"])
@login_required
def teletable():
    """Display teletext standings"""

    session["getTopTable"] = db.execute("SELECT ROW_NUMBER () OVER (ORDER BY pts DESC, gs - ga DESC, gs DESC) row_num, club_name, club_attr.club_id, rank, pld, gs, ga, (gs - ga) AS gd, pts, pos, pos_track FROM club_attr JOIN clubs on club_attr.club_id = clubs.club_id WHERE club_attr.club_id IN (SELECT rank FROM club_attr WHERE manager_id = ? AND rank < 11) ORDER BY pts DESC, gd DESC, gs DESC, pos ASC;",
                                        session["id"])

    session["getSubTable"] = db.execute("SELECT ROW_NUMBER () OVER (ORDER BY pts DESC, gs - ga DESC, gs DESC) row_num, club_name, club_attr.club_id, rank, pld, gs, ga, (gs - ga) AS gd, pts, pos, pos_track FROM club_attr JOIN clubs on club_attr.club_id = clubs.club_id WHERE club_attr.club_id IN (SELECT rank FROM club_attr WHERE manager_id = ? AND rank > 10 AND rank < 21) ORDER BY pts DESC, gd DESC, gs DESC, pos ASC;",
                                        session["id"])

    session["userTeam"] = db.execute("SELECT * FROM managers WHERE id = ?",
                                    session["id"])[0]['club_name']

    for club in session['getTopTable']:
        db.execute("UPDATE club_attr SET pos_track = :prev_pos, pos = :pos WHERE manager_id = :id AND club_id = :club_id",
                    prev_pos=club['pos'], pos=club['row_num'], id=session["id"], club_id=club["club_id"])
    
    for club in session['getSubTable']:
        db.execute("UPDATE club_attr SET pos_track = :prev_pos, pos = :pos WHERE manager_id = :id AND club_id = :club_id",
                    prev_pos=club['pos'], pos=club['row_num'] + 10, id=session["id"], club_id=club["club_id"])
    
    if session["getTopTable"][0]['pld'] < 18:
        if session["getTopTable"][0]['pld'] == 9:
            leaguePos = db.execute("SELECT pos FROM club_attr WHERE club_id=20 AND manager_id=?",
                                    session['id'])[0]['pos']
            if session['managerStats']['clubrank'] - leaguePos >= 5:
                if session['managerStats']['confidence'] <= 90:
                    session['managerStats']['confidence'] += 10
                else:
                    session['managerStats']['confidence'] = 100
                
                db.execute("UPDATE managers SET board_confidence = ? WHERE id = ?",
                           session['managerStats']['confidence'], session['id'])
    gotNews(session["id"])
    else:
        gotNews(session['id'], 21)
        gotNews(session['id'], 22)
        # add board confidence after a result and end of season reset

    return render_template('teletable.html',
                        getTopTable=session["getTopTable"],
                        getSubTable=session["getSubTable"],
                        userTeam=session["userTeam"])

@app.route("/standings", methods=["GET"])
@login_required
def standings():
    """Display current standings"""

    session["getStandings"] = db.execute("SELECT club_name, rank, pld, gs, ga, (gs - ga) AS gd, pts, pos, pos_track FROM club_attr JOIN clubs on club_attr.club_id = clubs.club_id WHERE club_attr.club_id IN (SELECT rank FROM club_attr WHERE manager_id = ? AND rank < 21) ORDER BY pts DESC, gd DESC, pos ASC;",
                                         session["id"])

    session["userTeam"] = db.execute("SELECT * FROM managers WHERE id = ?",
                                     session["id"])[0]['club_name']

    return render_template('standings.html',
                           getStandings=session["getStandings"],
                           userTeam=session["userTeam"])

@app.route("/buy", methods=["POST"])
@login_required
def buy():
    """Make player purchase"""

    session["pl_id"] = int(request.form.get("pl_id"))
    session["pl_cost"] = float(request.form.get("pl_cost"))
    session["cl_id"] = int(request.form.get("cl_id"))
    session["cl_rank"] = int(request.form.get("cl_rank"))
    session["pl_pos"] = request.form.get("pl_pos")
    session["squad_num"] = int(request.form.get("squad_num"))
    session["cl_name"] = request.form.get("cl_name")
    
    session["userClub"] = db.execute("SELECT * FROM managers JOIN club_attr ON managers.club_id = club_attr.club_id WHERE id = ?;",
                                   session["id"])[0]

    if session["cl_id"] == 21:
        session["news_id"] = 2.5
    else:
        session["news_id"] = 2
    
    # check that user has enough funds for purchase
    if session["pl_cost"] > session["userClub"]['budget']:
        flash(f"Sorry, we don\'t currently have the funds to buy that player - Glenn.", 'alert-danger')
        return redirect('/transfers')

    # check player rank to see if they'd be interested in move
    session['rankDiff'] = session['userClub']['rank'] - session["cl_rank"]
    if session['rankDiff'] > 5:
        if session['rankDiff'] < 8 and randint(1,10) > session['rankDiff'] + 1:
            pass
        else:
            gotNews(session['id'], 3, session['pl_id'])
            flash(f"It doesn\'t look like that player is interested - check your emails for details.", 'alert-danger')
            return redirect('/transfers')

    # if user has funds and offer accepted generate new player for selling club (if not a free agent & squad < 11)
    session['playerCount'] = db.execute("SELECT count(*) FROM player_attr WHERE club_id = ? AND manager_id = ?;", 
                                        session["cl_id"], session["id"])[0]
    if session["cl_id"] != 21:
        if session['playerCount']['count(*)'] < 11:
            session["newPlayer"] = makePlayer(session["pl_pos"], session["squad_num"], session["cl_name"])
            session["pl_stats"] = makeAttr("cl_name")
            session["getManagers"] = db.execute("SELECT * FROM managers;")
            for manager in session["getManagers"]:
                db.execute("INSERT INTO player_attr (manager_id, player_id, club_id, squad_num, age, speed, strength, technique, potential, handsomeness, ovr, value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", 
                            manager['id'], session["newPlayer"]['player_id'], session["cl_id"], session["squad_num"], session["pl_stats"]['age'], session["pl_stats"]['speed'], session["pl_stats"]['strength'], 
                            session["pl_stats"]['technique'], session["pl_stats"]['potential'], session["pl_stats"]['handsomeness'], session["pl_stats"]['ovr'], session["pl_stats"]['value'])
    
    # send success email, update player info and budget
    session["newBudget"] = round((session["userClub"]['budget'] - session["pl_cost"]),2)
    db.execute("UPDATE managers SET budget = ? WHERE id = ?",
                session["newBudget"], session["id"])

    gotNews(session['id'], session['news_id'], session['pl_id'])
    db.execute("UPDATE player_attr SET club_id = 20, squad_num = ? WHERE player_id = ? AND manager_id = ?;",
                session['playerCount']['count(*)'] + 1, session["pl_id"], session["id"])
    
    #  redirect to office page and display success message confirming transfer
    flash('Purchase successful. Your updated transfer budget is £' + str(session["newBudget"]) + 'm.',
            'alert-success')
    return redirect('/')


@app.route("/sell", methods=["POST"])
@login_required
def sell():
    """Make player sale"""
    session["pl_id"] = int(request.form.get("pl_id"))
    session["cl_id"] = int(request.form.get("cl_id"))
    session["sell_pl"] = db.execute("SELECT * FROM player_attr WHERE player_id = ? and manager_id = ?;",
                                        session['pl_id'], session['id'])[0]

    if session["cl_id"] == 21:
        session["pl_cost"] = float(request.form.get("pl_cost"))
        session["cl_name"] = request.form.get("cl_name")
    else:
        session["pl_cost"] = session['sell_pl']['value']
        session["cl_name"] = db.execute("SELECT club_name FROM clubs WHERE club_id = ?;",
                                        session['cl_id'])[0]['club_name']

    session["userClub"] = db.execute("SELECT * FROM managers JOIN club_attr ON managers.club_id = club_attr.club_id WHERE id = ?;",
                                     session["id"])[0]

    session['playerCount'] = db.execute("SELECT count(*) FROM player_attr WHERE club_id = 20 AND manager_id = ?;", 
                                         session["id"])[0]['count(*)']
    
    if session['playerCount'] < 11:
        #  squad too small - redirect to office page and display error message
        flash(f"Sorry, we don't have a big enough sqaud to let that player go - Glenn.", 'alert-danger')
        return redirect('/')

    # carry out transfer
    session["newBudget"] = round((session["userClub"]['budget'] + session["pl_cost"]),2)
    new_club = db.execute("SELECT * FROM player_attr WHERE club_id = ? AND manager_id = ?;",
                                     session['cl_id'], session['id'])

    db.execute("UPDATE managers SET budget = ? WHERE id = ?",
                session["newBudget"], session["id"])

    db.execute("UPDATE player_attr SET club_id = ? WHERE player_id = ? AND manager_id = ?;",
                session["cl_id"], session["pl_id"], session["id"])
    
    # prevent squad number clash
    for player in new_club:
        if player['squad_num'] == session["sell_pl"]['squad_num']:
            new_num = len(new_club)
            while any(player['squad_num'] == new_num for player in new_club):
                new_num += 1
            player['squad_num'] = new_num
            db.execute("UPDATE player_attr SET squad_num = ? WHERE player_id = ? AND manager_id = ?;",
                        player['squad_num'], player["player_id"], session["id"])
    

    #  redirect to office page and display success message confirming player release
    if session["cl_id"] == 21:
        flash('Player released. Your updated transfer budget is £' + str(session["newBudget"]) + 'm.',
              'alert-success')
    else:
        flash('Player sold to ' + session['cl_name'] + '. Your updated transfer budget is £' + str(session["newBudget"]) + 'm.',
              'alert-success')
    
    return redirect('/')


@app.route("/read", methods=["POST"])
@login_required
def read():
    """ Mark email as read """
    session['rstatus'] = int(request.form['rstatus'])
    session['mail_id'] = int(request.form['mail_id'])
    if session['rstatus'] > 0:
        db.execute("UPDATE news SET read = ? WHERE news_id = ?",
                    session['rstatus'], session['mail_id'])
        return jsonify(rstatus=session["rstatus"],
                       mail_id=session["mail_id"])


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
        session["clubname"] = rows[0]["club_name"]

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
        thisYear = date.today().year
        db.execute("INSERT INTO managers (username, hash, name, club_id, club_name, season, current_season) VALUES (?, ?, ?, 20, ?, ?, ?);", 
                   username, phash, name, clubname, thisYear, thisYear)

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
        generateFixtures(session["id"], session["club_name"], thisYear)

        #generate welcome email via news.py
        gotNews(session["id"], 1)
        
        # Redirect user to home page
        flash('Your sign-up was successful. Welcome aboard!', 'alert-success')
        return redirect("/")

    return apology("Oops, something went awry", 403)
