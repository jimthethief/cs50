from random import randint, choice, choices
from time import sleep
from cs50 import SQL

db = SQL("sqlite:///champgaffer.db")

# return avg ratings and star player for position
def posStats(posList):
    total = 0
    mx = 0
    for player in posList:
        total += player["ovr"]
        if player["ovr"] >= mx:
            star = player
            mx = player["ovr"]
    ovr = total / (len(posList))
    return ovr, star

# compare attacking star platers
def getStarAtk(md, at):
    if md['ovr'] > at['ovr']:
        return md
    else:
        return at 

# return team stats for match sim
def matchSetup(teamlineup, teamformation, teaminfo):

    defence = []
    midfield = []
    attack = []
    
    shape = teamformation.split("-")
    posCount = 0
    for player in range(posCount, (int(shape[0])+1)):
        defence.append(teamlineup[player])
    posCount += ((int(shape[0])) + 1) 
    for player in range(posCount, posCount + int(shape[1])):
        midfield.append(teamlineup[player])
    posCount += (int(shape[1]))
    for player in range(posCount, posCount + int(shape[2])):
        attack.append(teamlineup[player])
    posCount += (int(shape[2]))   

    defOvr, starDef = posStats(defence)
    slicedDef = defence[1:]
    midOvr, starMid = posStats(midfield)
    attOvr, starAtt = posStats(attack)
    starAtk = getStarAtk(starMid, starAtt)

    teamStats = {'club_id': teaminfo['club_id'], 'attack': attOvr, 'defence': defOvr, 'midfield': midOvr, 'consistency': teaminfo['ovr'], 'starAtk': starAtk['name'], 'starAtkRtg': starAtk['ovr'], 'starDef': starDef['name'], 'starDefRtg': starDef['ovr'], 'attendance': randint((teaminfo['capacity'] * teaminfo['attendance']), teaminfo['capacity']), 'capacity': teaminfo['capacity'], 'leaguepos': teaminfo['pos'], 'rival': teaminfo['rival']}     
    
    teamList = [slicedDef, midfield, [starMid], attack, [starAtt]]

    return teamStats, teamList

# boost attendances for rival matches
def attendanceBoost(homestats, awaystats):
    attendanceBoost = 0
    if abs(homestats['leaguepos'] - awaystats['leaguepos']) < 3:
        attendanceBoost += (homestats['attendance'] * 0.1)
    if homestats['rival'] == awaystats['club_id']:
        attendanceBoost += (homestats['attendance'] * 0.2)
    return round(attendanceBoost)


def simMatch(home, homeList, away, awayList):
    # gauge home advantage from attendance
    boost = attendanceBoost(home, away)
    attendance = min((home["attendance"] + boost), home['capacity'])
    homeadv = 0
    if attendance > (home["capacity"] * 0.8):
        homeadv = 0.8
    elif attendance > (home["capacity"] * 0.6):
        homeadv = 0.5
    else:
        homeadv = 0.1

    # compile average stats for home and away teams
    avgHome = (home["attack"] + home["defence"] + home["midfield"] + home["consistency"] + home["starAtkRtg"] + home["starAtkRtg"]) / 6
    avgAway = (away["attack"] + away["defence"] + away["midfield"] + away["consistency"] + away["starAtkRtg"] + away["starDefRtg"]) / 6

    # team head to head
    homeAtt = (((home["attack"] - away["defence"]) + (home["midfield"] - away["midfield"]) + (home["starAtkRtg"] - away["starDefRtg"])) + homeadv) / 3
    awayAtt = ((away["attack"] - home["defence"]) + (away["midfield"] - home["midfield"]) + (away["starAtkRtg"] - home["starDefRtg"])) / 3

    # simulate maximum number of goals home and away teams could score
    maxGlsHome = round((((avgHome + homeAtt + homeadv) / avgAway) * randint(5,7)) * (home["consistency"] / 20))
    maxGlsAway = round((((avgAway + awayAtt) / avgHome) * randint(5,7)) * (away["consistency"] / 20))
    
    # randomise score
    glsHome = randint(0, randint(round((maxGlsHome / 2)), maxGlsHome))
    glsAway = randint(0, randint(round((maxGlsAway / 2)), maxGlsAway))

    # who scored the goals? uses list returned from match setup function
    scoreWeights = [0.04, 0.18, 0.23, 0.3, 0.25]
    homeScorers = []
    awayScorers = []
    for goal in range(0, glsHome):
        scorer = choices(homeList, scoreWeights)
        homeScorers.append(choice(choice(scorer)))
    for goal in range(0, glsAway):
        scorer = choices(awayList, scoreWeights)
        awayScorers.append(choice(choice(scorer)))

    return glsHome, glsAway, homeScorers, awayScorers, attendance


"""
getFixtures =  db.execute("SELECT home, away FROM fixtures JOIN managers ON fixtures.manager_id = managers.id WHERE (managers.id = ? AND week = matchday) AND (home != managers.club_name AND away != managers.club_name);",
                            3)
results = []
fixture_id = 622
for fixture in getFixtures:
    homeSimName = fixture['home']
    awaySimName = fixture['away']
    homeSimInfo = db.execute("SELECT club_name, primary_colour, secondary_colour, attendance, capacity, ovr, formation, pos, rival, pts, gs, ga, clubs.club_id FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE clubs.club_name = ? AND manager_id = ?;",
                                homeSimName, 3)[0]

    homeSimTeam = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.manager_id = ? AND player_attr.club_id = ?;",
                                3, homeSimInfo["club_id"])[:11]

    awaySimInfo = db.execute("SELECT club_name, primary_colour, secondary_colour, attendance, capacity, ovr, formation, pos, rival, pts, gs, ga, clubs.club_id FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE clubs.club_name = ? AND manager_id = ?;",
                                awaySimName, 3)[0]

    awaySimTeam = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE player_attr.manager_id = ? AND player_attr.club_id = ?;",
                                3, awaySimInfo["club_id"])[:11]
    
    homeSimFormation = homeSimInfo['formation']
    awaySimFormation = awaySimInfo['formation']

    homeSim, homeSimTeamList = matchSetup(homeSimTeam, homeSimFormation, homeSimInfo)
    awaySim, awaySimTeamList = matchSetup(awaySimTeam, awaySimFormation, awaySimInfo)
    homeSimGls, awaySimGls, homeSimScorers, awaySimScorers, simAttendance = simMatch(homeSim, homeSimTeamList, awaySim, awaySimTeamList)
    
    print(f"{homeSimName}{homeSimGls} - {awaySimGls}{awaySimName}")

    if homeSimGls > awaySimGls:
        homeSimPts = 3
        awaySimPts = 0
    elif awaySimGls > homeSimGls:
        homeSimPts = 0
        awaySimPts = 3
    else:
        homeSimPts = 1
        awaySimPts = 1
    
    db.execute("UPDATE club_attr SET pld = :pld, gs = :gs, ga = :ga, pts = :pts WHERE manager_id = :id AND club_id = :club_id;",
                pld=17, gs=homeSimInfo['gs'] + homeSimGls, ga=homeSimInfo['ga'] + awaySimGls, 
                pts=homeSimInfo['pts'] + homeSimPts, id=3, club_id=homeSimInfo['club_id'])
            
    db.execute("UPDATE club_attr SET pld = :pld, gs = :gs, ga = :ga, pts = :pts WHERE manager_id = :id AND club_id = :club_id;",
                pld=17, gs=awaySimInfo['gs'] + awaySimGls, ga=awaySimInfo['ga'] + homeSimGls, 
                pts=awaySimInfo['pts'] + awaySimPts, id=3, club_id=awaySimInfo['club_id'])

    db.execute("UPDATE fixtures SET played = :played WHERE fixture_id = :fixture_id AND manager_id = :manager_id;",
                played=1, fixture_id=fixture_id, manager_id=3)
    
    fixture_id += 1

    for scorer in homeSimScorers + awaySimScorers:
        db.execute("INSERT INTO goals(manager_id, player_id, week, season) VALUES(:manager_id, :player_id, :week, :season);",
                    manager_id=3, player_id=scorer['player_id'], week=17, 
                    season=2)

    db.execute("UPDATE managers SET matchday = ? WHERE id = ?;",
                18, 3)
"""
