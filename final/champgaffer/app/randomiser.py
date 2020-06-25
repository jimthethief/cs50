from random import randint, choices, uniform, shuffle
from statistics import mean
from faker import Faker

import collections


ages = [randint(16,19), randint(20, 24), randint(24, 29), randint(30, 33), randint(34, 37), randint(38, 40)]
ageWeights = [0.2, 0.3, 0.35, 0.1, 0.08, 0.02]

attribute = [randint(1,5), randint(6,9), randint(10,12), randint(13, 14), randint(15, 16), randint(17, 18), 19, 20]
garbage = [0.2, 0.3, 0.25, 0.15, 0.05, 0.04, 0.01, 0]
low = [0.1, 0.2, 0.25, 0.3, 0.05, 0.05, 0.04, 0.01]
lowerMid= [0.05, 0.15, 0.2, 0.4, 0.1, 0.05, 0.04, 0.01]
mid = [0.04, 0.07, 0.2, 0.2, 0.2, 0.2, 0.06, 0.03]
upperMid = [0.02, 0.05, 0.07, 0.16, 0.3, 0.2, 0.15, 0.05]
top = [0.01, 0.04, 0.05, 0.1, 0.2, 0.3, 0.2, 0.1]
elite = [0, 0.01, 0.09, 0.05, 0.15, 0.2, 0.3, 0.2]
free = [0.1, 0.2, 0.2, 0.2, 0.125, 0.1, 0.05, 0.025]


def punterRating(ovr):
    if ovr >= 19:
        return elite
    elif ovr >= 17:
        return top
    elif ovr >= 15:
        return upperMid
    elif ovr >= 12:
        return mid
    elif ovr >= 10:
        return lowerMid
    elif ovr >= 7:
        return low
    else:
        return garbage
        

def playerValue(ovr, handsomeness, potential):
    values = [uniform(0.1,0.2), uniform(0.2,0.4), uniform(0.4,0.5), uniform(0.5,0.6), uniform(0.6,0.8), uniform(0.9, 1.2), uniform(1.3, 1.5), uniform(1.6, 2)]
    value = 0
    if ovr > 18:
        value = randint(13,15) + choices(values, punterRating(ovr))[0]
    elif ovr > 16:
        value = randint(8,12) + choices(values, punterRating(ovr))[0]
    elif ovr > 14:
        value = randint(5,8) + choices(values, punterRating(ovr))[0]
    elif ovr > 12:
        value = randint(3,7) + choices(values, punterRating(ovr))[0]
    elif ovr >= 10:
        value = randint(1,3) + choices(values, punterRating(ovr))[0]
    else:
        value = (ovr / 10) + uniform(value * 0.1, value * 0.4)
    if potential > 17:
        value += uniform(value * 0.1, value * 0.2)
    if handsomeness > 17 or handsomeness > ovr + 2:
        value += uniform(value * 0.2, value * 0.4)
    return round((value), 1)
   

nations = [
    {"nationality": "English", "nat_code": "en_GB", "flag": "eng.svg"}, 
    {"nationality": "Irish", "nat_code": "en_GB", "flag": "ire.svg"}, 
    {"nationality": "Scottish", "nat_code": "en_GB", "flag": "sco.svg"}, 
    {"nationality": "Welsh", "nat_code": "en_GB", "flag": "wal.svg"}, 
    {"nationality": "Japanese", "nat_code": "ja_JP", "flag": "jp.svg"}, 
    {"nationality": "Spanish", "nat_code": "es_ES", "flag": "es.svg"}, 
    {"nationality": "Brazilian", "nat_code": "pt_BR", "flag": "br.svg"}, 
    {"nationality": "Czech", "nat_code": "cs_CZ", "flag": "cr.svg"},
    {"nationality": "German", "nat_code": "de_DE", "flag": "de.svg"},
    {"nationality": "American", "nat_code": "en_US", "flag": "us.svg"},
    {"nationality": "Mexican", "nat_code": "es_MX", "flag": "mx.svg"},
    {"nationality": "French", "nat_code": "fr_FR", "flag": "fr.svg"},
    {"nationality": "Belgian", "nat_code": "nl_NL", "flag": "be.svg"},
    {"nationality": "Portuguese", "nat_code": "pt_PT", "flag": "pt.svg"},
    {"nationality": "Argentinian", "nat_code": "es_ES", "flag": "arg.svg"},
    {"nationality": "Italian", "nat_code": "it_IT", "flag": "it.svg"},
    {"nationality": "Dutch", "nat_code": "nl_NL", "flag": "nl.svg"},
    {"nationality": "Norwegian", "nat_code": "no_NO", "flag": "no.svg"},
    {"nationality": "Swedish", "nat_code": "sv_SE", "flag": "sv.svg"},
    {"nationality": "Polish", "nat_code": "pl_PL", "flag": "pl.svg"},
    {"nationality": "Turkish", "nat_code": "tr_TR", "flag": "tr.svg"},
    {"nationality": "Ghanaian", "nat_code": "tw_GH", "flag": "gh.svg"},
    {"nationality": "Australian", "nat_code": "en_NZ", "flag": "aus.svg"}
]

nationWeights = [10, 2, 5, 2, 0.7, 6, 1, 0.5, 5, 0.5, 0.5, 5, 4, 4, 1, 4, 5, 2, 3, 0.5, 0.5, 0.5, 0.5]


def nameFaker(nat_code):
    fake = Faker(nat_code)
    if nat_code == "ja_JP":  
        name = fake.first_romanized_name() + " " + fake.last_romanized_name()
    else:
        name = fake.first_name_male() + " " + fake.last_name()
    return name


Teams = {
    "Merseyside Mawlers": {"club_id": 1, "rank": 1, "primary-color": "Crimson", "secondary-color": "Gold", "ovr": randint(19, 20), "formation": "4-3-3", "manager": nameFaker("de_DE"), "desc": "As efficient as a German car.", "attendance": 0.7, "capacity": 54000, "rival": 2},
    "Lannister City": {"club_id": 2, "rank": 2, "primary-color": "LightSkyBlue", "secondary-color": "#1C2C5B", "ovr": randint(19, 20), "formation": "3-5-2", "manager": nameFaker("es_ES"), "desc": "Owned by an oil baron, probably.", "attendance": 0.5, "capacity": 56000, "rival": 6},
    "Kensington Gentlemen": {"club_id": 3, "rank": 3, "primary-color": "RoyalBlue", "secondary-color": "white", "ovr": randint(17, 18), "formation": "4-4-2", "manager": nameFaker(choices(nations, nationWeights)[0]['nat_code']), "desc": "Know how to play but don\'t like to get their shorts dirty.", "attendance": 0.6, "capacity": 42000, "rival": 5}, 
    "London Hipsters": {"club_id": 4, "rank": 4, "primary-color": "FireBrick", "secondary-color": "Azure", "ovr": randint(16, 17), "formation": "4-3-3", "manager": nameFaker(choices(nations, nationWeights)[0]['nat_code']), "desc": "Have the latest iPhone and know all the best coffee places.", "attendance": 0.5, "capacity": 60000, "rival": 9},
    "Celt Crabits": {"club_id": 5, "rank": 5, "primary-color": "white", "secondary-color": "SeaGreen", "ovr": randint(15, 17), "formation": "4-4-2", "manager": nameFaker("en_GB"), "desc": "Gie us a wee swally an haud yer wheesht.", "attendance": 0.7, "capacity": 60000, "rival": 3},
    "North United": {"club_id": 6, "rank": 6, "primary-color": "#DA291C", "secondary-color": "black", "ovr": randint(15, 17), "formation": "4-5-1", "manager": nameFaker("no_NO"), "desc": "Used to win everything before having an existential crisis.", "attendance": 0.4, "capacity": 76000, "rival": 2},
    "Feral Foxes": {"club_id": 7, "rank": 7, "primary-color": "#0053A0", "secondary-color": "#FDBE11", "ovr": randint(14, 15), "formation": "4-5-1", "manager": nameFaker("it_IT"), "desc": "Were strongly linked to crisps before they rebranded and won the league that time.", "attendance": 0.6, "capacity": 32000, "rival": 8},
    "Brummy Howlers": {"club_id": 8, "rank": 8, "primary-color": "#FDB913", "secondary-color": "black", "ovr": randint(12, 15), "formation": "4-3-3", "manager": nameFaker("pt_PT"), "desc": "Cause a few upsets. Mostly Portuguese.", "attendance": 0.5, "capacity": 32000, "rival": 7},
    "West Lamb": {"club_id": 9, "rank": 9, "primary-color": "#7C2C3b", "secondary-color": "#2DAFE5", "ovr": randint(12, 15), "formation": "4-4-2", "manager": nameFaker(choices(nations, nationWeights)[0]['nat_code']), "desc": "Try to play expansive football, revert to long balls when it doesn\'t work.", "attendance": 0.4, "capacity": 60000, "rival": 4},
    "North East Stripeys": {"club_id": 10, "rank": 10, "primary-color": "black", "secondary-color": "white", "ovr": randint(12, 14), "formation": "4-5-1", "manager": nameFaker("en_GB"), "desc": "They'd love it if they beat you.", "attendance": 0.6, "capacity": 53000, "rival": 17},
    "Yorkshire Flatcaps": {"club_id": 11, "rank": 11, "primary-color": "white", "secondary-color": "#FFCD00", "ovr": randint(11, 12), "formation": "3-5-2", "manager": nameFaker("es_ES"), "desc": "Ey up, we'll bring more cocker.", "attendance": 0.8, "capacity": 38000, "rival": 6},
    "Norfolk Budgies": {"club_id": 12, "rank": 12, "primary-color": "#fff200", "secondary-color": "#00A650", "ovr": 12, "formation": "4-4-2", "manager": nameFaker(choices(nations, nationWeights)[0]['nat_code']), "desc": "Where are you? Let\'s be \'avin\' you!", "attendance": 0.5, "capacity": 27000, "rival": 20},
    "Rocky Rovers": {"club_id": 13, "rank": 13, "primary-color": "#009EE0", "secondary-color": "white", "ovr": randint(12, 14), "formation": "4-3-3", "manager": "Tony Mohawk", "desc": "We won the league once, you know.", "attendance": 0.5, "capacity": 32000, "rival": 15},
    "Sherwood Goats": {"club_id": 14, "rank": 14, "primary-color": "white", "secondary-color": "#231F20", "ovr": randint(9, 11), "formation": "4-4-2", "manager": nameFaker(choices(nations, nationWeights)[0]['nat_code']), "desc": "Club with a proud history and an indifferent present.", "attendance": 0.4, "capacity": 34000, "rival": 16},
    "Claret Coopers": {"club_id": 15, "rank": 15, "primary-color": "#80BFFF", "secondary-color": "Maroon", "ovr": randint(7, 10), "formation": "4-4-2", "manager": nameFaker("en_GB"), "desc": "Above average height. Manager won\'t stand for anything fancy.", "attendance": 0.4, "capacity": 23000, "rival": 13},
    "Boozy Brewers": {"club_id": 16, "rank": 16, "primary-color": "#FDE92B", "secondary-color": "#231F20", "ovr": randint(6, 11), "formation": "4-5-1", "manager": nameFaker(choices(nations, nationWeights)[0]['nat_code']), "desc": "Love a good pint and smell faintly of marmite.", "attendance": 0.3, "capacity": 7000, "rival": 14},
    "Wearside Macks": {"club_id": 17, "rank": 17, "primary-color": "#EB172B", "secondary-color": "#211E1E", "ovr": randint(4, 6), "formation": "4-5-1", "manager": nameFaker(choices(nations, nationWeights)[0]['nat_code']), "desc": "Things can only get better... Oh, wait.", "attendance": 0.3, "capacity": 49000, "rival": 11},
    "Middlebrook Mill": {"club_id": 18, "rank": 18, "primary-color": "white", "secondary-color": "#263C7E", "ovr": randint(2, 5), "formation": "4-3-3", "manager": nameFaker("en_GB"), "desc": "Deeply in debt but struggling on.", "attendance": 0.3, "capacity": 29000, "rival": 19},
    "Seaside Satsumas": {"club_id": 19, "rank": 19, "primary-color": "#FF5F00", "secondary-color": "white", "ovr": randint(1, 4), "formation": "4-4-2", "manager": nameFaker("en_GB"), "desc": "The Vegas of the North but without the money or glamour.", "attendance": 0.2, "capacity": 17000, "rival": 18},
    "new_user": {"club_id": 20, "rank": 20, "primary-color": "#2E86C1", "secondary-color": "#FFC300", "ovr": randint(14, 15), "manager": "Mr. Noname", "formation": "4-4-2", "desc": "Can you transform these plucky underdogs into world beaters?", "attendance": 0.5, "capacity": 22000, "rival": 12}, 
    "Free Agents": {"club_id": 21, "rank": 21, "primary-color": "white", "secondary-color": "black", "ovr": choices(attribute, free)[0], "formation": "10-10-10", "manager": nameFaker(choices(nations, nationWeights)[0]['nat_code']), "desc": "This player is available on a free.", "attendance": 0, "capacity": 0, "rival": 0}
}

def makePlayer(pos, num, team):
    player = dict.fromkeys(["player_id", "club_id", "clubname", "squadnum", "name", "nationality", "nat_code", "flag", "pos"])
    player["club_id"] = Teams[team]['club_id']
    player["clubname"] = team
    player["squadnum"] = num
    nationinfo = choices(nations, nationWeights)[0]
    player["nationality"] = nationinfo['nationality']
    player["nat_code"] = nationinfo['nat_code']
    player["name"] = nameFaker(player['nat_code'])
    player["flag"] = nationinfo['flag']
    player["pos"] = pos
       
    return player


def makeSquad(team):
    formation = Teams[team]["formation"].split("-")
    for pos in range(1):
        gk = makePlayer("GK", team)
        squad.append(gk)
    for pos in range(0, int(formation[0])):
        df = makePlayer("DEF", team)
        squad.append(df)
    for pos in range(0, int(formation[1])):
        md = makePlayer("MID", team)
        squad.append(md)
    for pos in range(0, int(formation[2])):
        at = makePlayer("ATT", team)
        squad.append(at)
    
    return squad


def makeAttr(team):
    pl_attr = dict.fromkeys(["player_id", "club_id", "age", "speed", "strength", "technique", "potential", "handsomeness", "ovr", "value"])
    pl_attr["club_id"] = Teams[team]['club_id']
    pl_attr["speed"] = choices(attribute, punterRating(Teams[team]['ovr']))[0]
    pl_attr["strength"] = choices(attribute, punterRating(Teams[team]['ovr']))[0]
    pl_attr["technique"] = choices(attribute, punterRating(Teams[team]['ovr']))[0]
    pl_attr["potential"] = choices(attribute, punterRating(Teams[team]['ovr']))[0]
    pl_attr["handsomeness"] = choices(attribute, punterRating(Teams[team]['ovr']))[0]
    pl_attr["ovr"] = mean([pl_attr['speed'], pl_attr['strength'], pl_attr['technique'], pl_attr['potential'], pl_attr['handsomeness']]) 
    pl_attr["value"] = playerValue(pl_attr['ovr'], pl_attr['handsomeness'], pl_attr['potential'])
    pl_attr["age"] = choices(ages, ageWeights)[0]

    return pl_attr

def roundRobin(teams):
    """ Create a schedule for the teams in the list and return it"""
    firstMeet = []
    secondMeet = []
    if len(teams) % 2 == 1: teams = teams + [None]
    # manipulate map instead of list itself
    # takes advantage of even/odd indexes to determine home vs. away
    shuffle(teams)
    n = len(teams)
    map = list(range(n))
    mid = n // 2
    for i in range(n-1):
        l1 = map[:mid]
        l2 = map[mid:]
        l2.reverse()
        r1 = []
        r2 = []
        for j in range(mid):
            t1 = teams[l1[j]]
            t2 = teams[l2[j]]
            if j == 0 and i % 2 == 1:
                # flip the first match only, every other round
                # (this is because the first match always involves the last player in the list)
                r1.append((t2, t1))
                r2.append((t1, t2))
            else:
                r1.append((t1, t2))
                r2.append((t2,t1))
        firstMeet.append(r1)
        secondMeet.append(r2)
        # rotate list by n/2, leaving last element at the end
        map = map[mid:-1] + map[:mid] + map[-1:]
    
    # combine first and second meeting into schedule
    schedule = firstMeet + secondMeet

    return schedule


