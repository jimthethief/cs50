from randomiser import Teams, makeSquad, roundRobin
from random import choices, randint
from news import getStory

from cs50 import SQL

db = SQL("sqlite:///champgaffer.db")


def generateTeams():
    # add teams from randomiser into database
    for team in Teams:
        db.execute("INSERT INTO clubs (club_name, primary_colour, secondary_colour, manager, desc, capacity, rival) VALUES (?, ?, ?, ?, ?, ?, ?);", 
                    team, Teams[team]['primary-color'], Teams[team]['secondary-color'], Teams[team]['manager'], 
                    Teams[team]['desc'], Teams[team]['capacity'], Teams[team]['rival'])


def generateSquads():
    # generate squads for each club using randomiser functions
    getClubs = db.execute("SELECT * FROM clubs;")
    for row in getClubs:
        club = row["club_name"]
        squad = makeSquad(club)
        for player in squad:
            db.execute("INSERT INTO players (starter_club, name, nationality, flag, pos) VALUES (?, ?, ?, ?, ?);", 
                    club, player["name"], player["nationality"], player["flag"], player["pos"])


def generatePlayerAttributes(user, players):
    for row in players:
        club = row["starter_club"]
        getClub = db.execute("SELECT * FROM clubs WHERE club_name = ?;", club)[0]['club_id']
        player = randomiser.makeAttr(club)
        db.execute("INSERT INTO player_attr (manager_id, player_id, club_id, age, speed, strength, technique, potential, handsomeness, ovr, value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", 
                    user, row['player_id'], getClub, player['age'], player['speed'], player['strength'], player['technique'], 
                    player['potential'], player['handsomeness'], player['ovr'], player['value'])


def generateClubAttributes(user, clubs):
    for row in clubs:
            club = row['club_name']
            db.execute("INSERT INTO club_attr (manager_id, club_id, rank, ovr, formation, attendance) VALUES (?, ?, ?, ?, ?, ?);", 
                        user, row['club_id'], Teams[club]['rank'], Teams[club]['ovr'],
                        Teams[club]['formation'], Teams[club]['attendance'])


def generateFixtures(user, clubname, season):
    
    # query db for list of team names in order of rank
    clubList = db.execute("SELECT clubs.club_name FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE club_attr.manager_id = ? AND clubs.club_id < 21 ORDER BY club_attr.rank;",
                          user)

    # initialise user clubname
    for club in clubList:
        if club['club_name'] == 'new_user':
            club['club_name'] = clubname
    
    # generate fixtures for top league (10 highest ranked teams)
    premFixtures = roundRobin(clubList[:10])

    matchday = 0
    for week in premFixtures:
        matchday += 1
        for fixture in week:
            home = fixture[0]['club_name']
            away = fixture[1]['club_name']
            db.execute("INSERT INTO fixtures (manager_id, season, week, home, away) VALUES (?, ?, ?, ?, ?);",
                       user, season, matchday, home, away)

    # generate fixtures bottom league (10 lowest ranked teams)
    champFixtures = roundRobin(clubList[10:])

    matchday = 0
    for week in champFixtures:
        matchday += 1
        for fixture in week:
            home = fixture[0]['club_name']
            away = fixture[1]['club_name']
            db.execute("INSERT INTO fixtures (manager_id, season, week, home, away) VALUES (?, ?, ?, ?, ?);",
                       user, season, matchday, home, away)


def getUserSquad(user):
    playerList = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE manager_id = ? AND club_id = 20;",
                            user)
    return playerList


def getUserPlayer(user):
    player = choices(getUserSquad(user))
    return player


def getRandomClub(user):
    clubs = db.execute("SELECT * FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE manager_id = ? AND clubs.club_id < 20;",
                       user)
    return choices(clubs)
    
# returns news story from news.getStory function 7/10 times - specific news stories can be selected via second argument
def gotNews(user, default=0):

    anyNews = randint(0,10)
    
    if anyNews > 3:
        userClub = db.execute("SELECT * FROM managers JOIN club_attr ON managers.id = club_attr.manager_id WHERE managers.id = ? AND club_attr.club_id = 20;",
                          user)
    
        currentNews = db.execute("SELECT * FROM news JOIN managers on news.manager_id = managers.id WHERE id = ?",
                            user)

        message = getStory(userClub, default)

        # if news item has already been delivered in current season, generate another until no match (max 20 loops)
        loopCount = 0
        while any(d.get('Mail_id', None) == message['Mail_id'] for d in currentNews):
            if loopCount > 20:
                break
            else:
                message = getStory(userClub, default)
                loopCount += 1

        db.execute("INSERT INTO news (manager_id, player_id, club_id, message_id, sender, subject, body) VALUES (?, ?, ?, ?, ?, ?, ?);",
                       user, message['Player_id'], message['Club_id'], message['Mail_id'], message['Sender'], message['Subject'], message['Body'])
            
    else:
        return False
    

gotNews(3, 1)


