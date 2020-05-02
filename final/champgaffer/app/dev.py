import cs50
from random import randint
from time import sleep

brfc = {"attack": 15, "defence": 14, "midfield": 15, "consistency": 12, "starAtk": "Bradley Dack", "starAtkRating": 17, "starDef": "Daragh Lenihan", "starDefRating": 16, "attendence": randint(13000, 18000), "capacity": 32000}
bfc = {"attack": 13, "defence": 15, "midfield": 12, "consistency": 10, "starAtk": "Ashley Barnes", "starAtkRating": 16, "starDef": "Nick Pope", "starDefRating": 16, "attendence": randint(15000, 17000), "capacity": 20000}

home = brfc
away = bfc
attendanceBoost = 5000
attendance = (home["attendence"] + attendanceBoost)
print (attendance)
homeadv = 0
if attendance > (home["capacity"] * 0.8):
    homeadv = 0.8
elif attendance > (home["capacity"] * 0.6):
    homeadv = 0.5
else:
    homeadv = 0.1


homeAtt = (((home["attack"] - away["defence"]) + (home["midfield"] - away["midfield"]) + (home["starAtkRating"] - away["starDefRating"])) + homeadv) /3
awayAtt = ((away["attack"] - home["defence"]) + (away["midfield"] - home["midfield"]) + (away["starAtkRating"] - home["starDefRating"])) / 3

print(str(round(homeAtt)) + "  v  " + str(round(awayAtt)))
print((away["consistency"] / 20))
print((home["consistency"] / 20))

avgHome = (home["attack"] + home["defence"] + home["midfield"] + home["consistency"] + home["starAtkRating"] + home["starAtkRating"]) / 6
print (f"avgHome: {avgHome}")
avgAway = (away["attack"] + away["defence"] + away["midfield"] + away["consistency"] + away["starAtkRating"] + away["starDefRating"]) / 6
print (f"avgAway: {avgAway}")

maxGlsHome = round((((avgHome + homeAtt + homeadv) / avgAway) * randint(5,9)) * (home["consistency"] / 20))
maxGlsAway = round((((avgAway + awayAtt) / avgHome) * randint(5,9)) * (away["consistency"] / 20))
print (f"maxGlsHome: {maxGlsHome}")
print (f"maxGlsAway: {maxGlsAway}")
glsHome = randint(0, randint(round((maxGlsHome / 2)), maxGlsHome))
glsAway = randint(0, randint(round((maxGlsAway / 2)), maxGlsAway))

print(f"Rovers: {glsHome}")
print(f"Burnley: {glsAway}")

added = (randint(90,95))
homeScore = 0
awayScore = 0
minutes = 0
ft = randint(90, added)
for mins in range(0, ft):
    minutes = randint(mins, ft)
    if homeScore < glsHome and minutes == mins:
        minutes = randint(minutes, ft)
        homeScore += 1
        print(f"{mins}: GOAL!!! Rovers... {homeScore} - {awayScore}!")
        sleep(0.5)
    if awayScore < glsAway and minutes == mins:
        minutes = randint(minutes, ft)
        awayScore += 1
        print(f"{mins}: GOAL!!! Burnley... {homeScore} - {awayScore}!")
        sleep(0.5)
    print (f"{mins}...")
    sleep(0.05)
print(f"Final Score: Blackburn {homeScore} - {awayScore} Burnley")

"""maxGlsHome = (((home["attack"] - away["defense"]) + (home["midfield"] - away["midfield"]) + (home["starrating"] - away["defense"])) * homeadv) * 2
maxGlsAway = ((away["attack"] - home["defense"]) + (away["midfield"] - home["midfield"]) + (away["starrating"] - home["defense"])) * 2
"""

#for mins in range(1,90):
#print (homeAtt)
#print (awayAtt)