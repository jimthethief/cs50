from random import randint, choice, choices
from time import sleep
from cs50 import SQL

db = SQL("sqlite:///champgaffer.db")

def posStats(posList):
    """Return avg ratings and star player for position"""

    total = 0
    mx = 0
    for player in posList:
        total += player["ovr"]
        if player["ovr"] >= mx:
            star = player
            mx = player["ovr"]
    ovr = total / (len(posList))
    return ovr, star


def getStarAtk(md, at):
    """Compare attacking star players"""

    # return player with highest 'ovr' stat
    if md['ovr'] > at['ovr']:
        return md
    # return attacker if 'ovr' stats identical
    else:
        return at 


def matchSetup(teamlineup, teamformation, teaminfo):
    """Return club and player stats to set up match"""
    defence = []
    midfield = []
    attack = []
    
    # add players to position list according to teamformation
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

    # add player stats to variables
    defOvr, starDef = posStats(defence)
    slicedDef = defence[1:]
    midOvr, starMid = posStats(midfield)
    attOvr, starAtt = posStats(attack)
    starAtk = getStarAtk(starMid, starAtt)

    # compile team stats in dictionary
    teamStats = {'club_id': teaminfo['club_id'], 'attack': attOvr, 'defence': defOvr, 'midfield': midOvr, 'consistency': teaminfo['ovr'], 'starAtk': starAtk['name'], 'starAtkRtg': starAtk['ovr'], 'starDef': starDef['name'], 'starDefRtg': starDef['ovr'], 'attendance': randint((teaminfo['capacity'] * teaminfo['attendance']), teaminfo['capacity']), 'capacity': teaminfo['capacity'], 'leaguepos': teaminfo['pos'], 'rival': teaminfo['rival']}     
    
    # compile player stats for each position in list
    teamList = [slicedDef, midfield, [starMid], attack, [starAtt]]

    return teamStats, teamList


def attendanceBoost(homestats, awaystats):
    """Boost attendances for rival matches"""

    attendanceBoost = 0
    if abs(homestats['leaguepos'] - awaystats['leaguepos']) < 3:
        attendanceBoost += (homestats['attendance'] * 0.1)
    if homestats['rival'] == awaystats['club_id']:
        attendanceBoost += (homestats['attendance'] * 0.2)

    return round(attendanceBoost)


def simMatch(home, homeList, away, awayList):
    """Simulate match using home and away stats"""

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


