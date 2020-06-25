from randomiser import Teams, makeSquad, makePlayer, makeAttr, playerValue, roundRobin
from random import choices, randint
from news import getStory

from cs50 import SQL

db = SQL("sqlite:///champgaffer.db")


def generateTeams():
    """intial database seeding - add teams from randomiser into database"""

    for team in Teams:
        db.execute("INSERT INTO clubs (club_name, primary_colour, secondary_colour, manager, desc, capacity, rival) VALUES (?, ?, ?, ?, ?, ?, ?);", 
                    team, Teams[team]['primary-color'], Teams[team]['secondary-color'], Teams[team]['manager'], 
                    Teams[team]['desc'], Teams[team]['capacity'], Teams[team]['rival'])


def generateSquads():
    """initial database seeding - generate squads for each club using randomiser functions"""

    getClubs = db.execute("SELECT * FROM clubs;")
    for row in getClubs:
        club = row["club_name"]
        squad = makeSquad(club)
        for player in squad:
            db.execute("INSERT INTO players (starter_club, name, nationality, flag, pos) VALUES (?, ?, ?, ?, ?);", 
                        club, player["name"], player["nationality"], player["flag"], player["pos"])


def generatePlayerAttributes(user, players):
    """set player attributes for new users"""

    for row in players:
        club = row["starter_club"]
        getClub = db.execute("SELECT * FROM clubs WHERE club_name = ?;", club)[0]['club_id']
        player = makeAttr(club)
        db.execute("INSERT INTO player_attr (manager_id, player_id, club_id, age, speed, strength, technique, potential, handsomeness, ovr, value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", 
                    user, row['player_id'], getClub, player['age'], player['speed'], player['strength'], player['technique'], 
                    player['potential'], player['handsomeness'], player['ovr'], player['value'])


def generateClubAttributes(user, clubs):
    """Set club attributes and player squad numbers for new users"""

    for row in clubs:
            club = row['club_name']
            club_id = row['club_id']
            db.execute("INSERT INTO club_attr (manager_id, club_id, rank, ovr, formation, attendance, pos_track, pos) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", 
                        user, row['club_id'], Teams[club]['rank'], Teams[club]['ovr'],
                        Teams[club]['formation'], Teams[club]['attendance'], Teams[club]['rank'], Teams[club]['rank'])

            # set player squad numbers
            if club_id < 21:
                squadnum = 1
                for player in db.execute("SELECT * FROM player_attr WHERE manager_id = ? AND club_id = ?;", user, club_id):
                    db.execute("UPDATE player_attr SET squad_num = ? WHERE player_id = ? AND manager_id = ?;", squadnum, player['player_id'], user)
                    squadnum += 1
                

def generateFixtures(user, clubname, season):
    """Create new fixtures for given user each season"""

    # check database for previous user fixture list and remove if exists
    if db.execute("SELECT * FROM fixtures WHERE manager_id = ?;", user):
        db.execute("DELETE FROM fixtures WHERE manager_id = ?;", user)

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


def updatePlayerAttributes(user):
    """Update player attributes at the end of each season"""

    players = db.execute("SELECT * FROM player_attr WHERE manager_id = ?;", user)
    for row in players:
        # separate improvable attributes from search
        attributes = dict.fromkeys(["age", "spd", "str", "tech", "hand"])
        attributes['age'] = row['age'] + 1
        attributes['spd'] = row['speed']
        attributes['str'] = row['strength']
        attributes['tech'] = row['technique']
        attributes['hand'] = row['handsomeness']

        # decrease all attributes for older players
        if attributes['age'] > 30:
            if row['handsomeness'] > 1:
                attributes['hand'] -= 1
            for key, stat in attributes.items():
                if row['potential'] < 18:
                    if stat > 1:
                        attributes[key] -= randint(0,1)
                else:
                    if randint(0,1) == 1:
                        if stat > 1:
                            attributes[key] -= randint(0,1)

        # increase improvable attributes for younger players with potential
        if row['potential'] > 18 and row['age'] < 27:
            if row['handsomeness'] < 20:
                attributes['hand'] += 1
            for key, stat in attributes.items():
                if stat <= 16:
                    attributes[key] += randint(1,2)
                elif stat < 20:
                    attributes[key] += randint(0,1)
        elif row['potential'] > 16 and row['age'] < 27:
            if row['handsomeness'] < 20:
                attributes['hand'] += randint(0,1)
            for key, stat in attributes.items():
                if stat <= 17:
                    attributes[key] += randint(0,1)
        elif row['potential'] > 14 and row['age'] < 29:
            for key, stat in attributes.items():
                if randint(1,2) == 2:
                    if stat <= 16:
                        attributes[key] += randint(0,1)

        # calculate new ovr rating and value
        ovr = round(((attributes['spd'] + attributes['str'] + attributes['tech'] + attributes['hand'] + row['potential']) / 5), 1)
        val = playerValue(ovr, attributes['hand'], row['potential'])

        db.execute("UPDATE player_attr SET age = :age, speed = :spd, strength = :str, technique = :tech, handsomeness = :han, ovr = :ovr, value = :val WHERE player_id = :pl_id AND manager_id = :man_id;", 
                    age=attributes['age'], spd=attributes['spd'], str=attributes['str'], tech=attributes['tech'], han=attributes['hand'], ovr=ovr, val=val, pl_id=row['player_id'], man_id=user)


def gotNews(user, news_id=0, pl_id=0):
    """Return specific or random news story"""

    anyNews = randint(0,10)
    
    # return random or specified snews item 
    if anyNews > 3 or news_id != 0:
        userClub = db.execute("SELECT * FROM managers JOIN club_attr ON managers.id = club_attr.manager_id WHERE managers.id = ? AND club_attr.club_id = 20;",
                          user)
    
        currentNews = db.execute("SELECT * FROM news JOIN managers on news.manager_id = managers.id WHERE id = ?",
                            user)

        message = getStory(userClub, news_id, pl_id)

        # if news item has already been delivered in current season, generate another until no match (max 20 loops)
        loopCount = 0
        while any(d.get('Mail_id', None) == message['Mail_id'] for d in currentNews) and message['Mail_id'] > 6:
            if loopCount > 20:
                break
            else:
                message = getStory(userClub, news_id, pl_id)
                loopCount += 1
        
        db.execute("INSERT INTO news (manager_id, player_id, club_id, message_id, sender, subject, body, offer) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                       user, message['Player_id'], message['Club_id'], message['Mail_id'], message['Sender'], message['Subject'], message['Body'], message['Offer'])
    else:
        return False
