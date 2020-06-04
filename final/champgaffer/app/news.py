from randomiser import playerValue
from random import randint, uniform, choices

from cs50 import SQL

db = SQL("sqlite:///champgaffer.db")

def getUserSquad(user):
    playerList = db.execute("SELECT * FROM players JOIN player_attr ON players.player_id = player_attr.player_id WHERE manager_id = ? AND club_id = 20;",
                            user)
    return playerList


def getUserPlayer(user, pl_id=0):
    if pl_id == 0:
        player = choices(getUserSquad(user))
    else:
        player = db.execute("SELECT * FROM players JOIN player_attr on players.player_id = player_attr.player_id JOIN clubs ON clubs.club_id = player_attr.club_id WHERE players.player_id = ? AND player_attr.manager_id = ?;",
                            pl_id, user)
    return player


def getRandomClub(user):
    clubs = db.execute("SELECT * FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE manager_id = ? AND clubs.club_id < 20;",
                       user)
    return choices(clubs)

def getClubByPos(user, pos):
    club = db.execute("SELECT * FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE manager_id = ? AND clubs_attr.pos = ?;",
                      user, pos)[0]
    return club

# returns random news story, taking dictionary as an argument - generated by database query in generator.gotNews(user) function
def getStory(clubDict, news_id, pl_id):
    userId = clubDict[0]['id']
    firstName = clubDict[0]['name'].split()[0].capitalize()

    Story = dict.fromkeys(["Mail_id", "Sender", "Subject", "Body", "Player_id", "Club_id"])
    if news_id != 0:
        item = news_id
    else:
        item = randint(4,20)

    Story['Mail_id'] = item
    Story['Player_id'] = 0
    Story['Club_id'] = 0
     
    if item == 1:
        if clubDict[0]['current_season'] - clubDict[0]['season'] == 0:
            Story['Sender'] = "The Chairman"
            Story['Subject'] = "Welcome to the club!"
            Story['Body'] = f"Hi {firstName},\n\nGreat to have you on board! We're confident that you're the right man to take the team forward. Anything less than a mid-table finish this season would be really disappointing. As we discussed in the interview, we're happy to invest - so we've allocated £{clubDict[0]['budget']}M as transfer funds. Good luck!\n\nWarm Regards,\nGlenn\n"
        else:
            Story['Sender'] = "The Chairman"
            Story['Subject'] = f"{clubDict[0]['current_season']} Expectations"
            if clubDict[0]['rank'] > 3:
                Story['Body'] = f"Hi {firstName},\n\nThanks yet again for working so hard to make last season a success. I never doubted that you're the man for the job. Same again this time around please {firstName} - we want to be challenging for that title! We're giving you £{clubDict[0]['budget']}M in the transfer kitty to keep us competetive.\n\nStay Classy,\nGlenn\n"   
            elif clubDict[0]['rank'] > 7:
                Story['Body'] = f"Hi {firstName},\n\nWe had a good showing last time out - it looks like we're on the right track! We want to make sure that we're moving forward, so we're providing £{clubDict[0]['budget']}M for new players.\n\nKeep it real,\n\nGlenn\n"
            elif clubDict[0]['rank'] > 11:
                Story['Body'] = f"Hi {firstName},\n\nIt's great to be in the top league isn't it? We'd very much like to get comfortable here, so I want you to concentrate on steadying the ship this year. I've put £{clubDict[0]['budget']}M aside for transfers.\n\nGood luck champ,\nGlenn\n"
            elif clubDict[0]['rank'] > 16:
                Story['Body'] = f"Hi {firstName},\n\nLast season was so-so but I think that we can do better. Let's give the fans something to shout about this season and push for promotion. I've put £{clubDict[0]['budget']}M into the transfer account for you to play with. Let's do this!\n\nWarm Regards,\nGlenn\n"
            else:
                Story['Body'] = f"Hi {firstName},\n\nI think we can both agree that last season was a little disappointing. We expect at least a mid-table finish this time around to keep things stable. We've allocated £{clubDict[0]['budget']}M to spend on players. Spend it wisely and let's get cracking!\n\nWarm Regards,\nGlenn\n"
    else:
        if item > 3 and item < 7:
            club = getRandomClub(userId)[0]
            Story['Club_id'] = club['club_id']

        if item > 3 and item < 12:
            player = getUserPlayer(userId)[0]
            stats = f"{player['name']}: Age: {player['age']} // Ovr: {player['ovr']} // Value: {player['value']}\n"
            Story['Player_id'] = player['player_id']

        if item == 2:
            player = getUserPlayer(userId, pl_id)[0]
            budget = clubDict[0]['budget']
            Story['Player_id'] = pl_id
            Story['Club_id'] = player['club_id']
            Story['Sender'] = "The Chairman"
            Story['Subject'] = f"FW: Transfer Offer - {player['name']}"
            if randint(1,2) == 1:
                Story['Body'] = f"Hi {firstName},\n\nOur offer for {player['name']} was successful! See below message from {player['club_name']}\'s manager. Our transfer budget is now £{budget}m. \n\nHi Glenn\n\nWe've reviewed the offer for {player['name']} and think that it is fair. We're reluctant to let him go but he's keen to join you - look after him.\n\nBest,\n{player['manager']}\n"
            else:
                Story['Body'] = f"Hi {firstName},\n\nLooks like I'm getting my chequebook out! {player['name']} will be joining the squad this week. We have £{budget}m left in transfer funds. Here's what {player['club_name']}\'s manager had to say:\n\nHi Glenn\n\nI'd like to keep {player['name']} he's pushing for the move and our chairman wants to sell so we're going to accept your offer. I just hope he has a stinker when we play you!\n\nBest,\n{player['manager']}\n"

        elif item == 2.5:
            player = getUserPlayer(userId, pl_id)[0]
            budget = clubDict[0]['budget']
            Story['Player_id'] = pl_id
            Story['Club_id'] = player['club_id']
            Story['Sender'] = "The Chairman"
            Story['Subject'] = f"FW: Free Transfer - {player['name']}"
            if randint(1,2) == 1:
                Story['Body'] = f"Hi {firstName},\n\nThese \'free transfers\' aren't as free as they used to be, I'll tell you that for a signing on fee.\n\nAnyway, {player['name']} seems happy and he'll be joining up with the squad immediately. We have £{budget}m left in the transfer kitty.\n\nWarm Regards,\nGlenn\n"
            else:
                Story['Body'] = f"Hi {firstName},\n\n{player['name']} has accepted our offer and is on his way to the club as I type.\n\nI'll trust your judgement on this one, hopefully he'll add something to the squad. We have £{budget}m left in transfer funds.\n\nWarm Regards,\nGlenn\n"

        elif item == 3:
            player = getUserPlayer(userId, pl_id)[0]
            Story['Player_id'] = pl_id
            Story['Club_id'] = player['club_id']
            Story['Sender'] = "The Chairman"
            Story['Subject'] = f"Transfer Offer - {player['name']}"
            if randint(1,2) == 1:
                Story['Body'] = f"Hi {firstName},\n\n{player['name']} isn\'t even slightly interested in coming to our club - his agent basically laughed at me. Maybe aim a bit lower next time.\nBest,\n\nGlenn\n"
            else:
                Story['Body'] = f"Hi {firstName},\n\n{player['name']} has politely declined to join the club. {player['club_name']}\'s manager said that it was a decent offer but the player is quite settled where he is. I think that we\'ll have to look at other targets.\n\nWarm Regards,\nGlenn\n"

        elif item == 4: 
            Story['Sender'] = club['manager']
            Story['Subject'] = f"Transfer Offer - {player['name']}"
            Story['Body'] = f"Hi {firstName},\n\nI like the look of {player['name']} and want to recruit him for {club['club_name']}. We're a bit hard up at the minute but I've pushed the chairman hard and we can stretch to £{round(playerValue(player['ovr'], player['handsomeness'], player['potential']) * uniform(0.5,0.7),1)}M. What do you think?\n\nRegards,\n{club['manager']}\n\n{stats}\n"
        
        elif item == 5:
            Story['Sender'] = club['manager']
            Story['Subject'] = f"Transfer Offer - {player['name']}"
            Story['Body'] = f"Hi {firstName},\n\nWe're looking to rebuild the squad at {club['club_name']} and I think that {player['name']} would be a great addition for us. Is he available? The chairman's being generous with this one so we can offer up to £{round(playerValue(player['ovr'], player['handsomeness'], player['potential']) * uniform(1.2, 1.8), 1)}m.\n\nThanks,\n{club['manager']}\n\n{stats}\n"
        
        elif item == 6:
            Story['Sender'] = club['manager']
            Story['Subject'] = f"Transfer Offer - {player['name']}"
            Story['Body'] = f"Hi {firstName},\n\nI've been admiring {player['name']} for a while now and would like to bring him to {club['club_name']}. How does £{playerValue(player['ovr'], player['handsomeness'], player['potential'])}M sound?\n\nThanks,\n{club['manager']}\n\n{stats}\n"
        
        elif item == 7:
            Story['Sender'] = "The Chairman"
            Story['Subject'] = player['name']
            Story['Body'] = f"Hi {firstName},\n\n{player['name']} has been out on the town again. It doesn't seem to be affecting his performances but apparently his moves are atrocious. Could you offer a quiet word of advice? And maybe a few dance lessons.\n\nWarm Regards,\nGlenn\n"

        elif item == 8:
            Story['Sender'] = "The Chairman"
            Story['Subject'] = player['name']
            Story['Body'] = f"Hi {firstName},\n\n{player['name']} has been sulking about the place recently and it's bringing me down. Could you see what is bothering with him? Also, have you seen my stapler? Morag only got me a new one on the last stationery order and its already gone AWOL.\n\nWarm Regards,\nGlenn\n"
        
        elif item == 9:
            Story['Sender'] = "The Chairman"
            Story['Subject'] = player['name']
            Story['Body'] = f"Hi {firstName},\n\nThe locker room showers are dripping again and our water bill is going to be through the roof. {player['name']}'s uncle is a plumber if I remember rightly. Could you ask him what he'd charge to have a look at it?\n\nWarm Regards,\nGlenn\n"

        elif item == 10:
            Story['Sender'] = "Head Coach"
            Story['Subject'] = player['name']
            Story['Body'] = f"Hi {firstName},\n\nI've been really impressed with {player['name'].split()[0]} in training this week gaffer. Did you see that overhead kick?! I'm not sure that it warranted the obscenity of the celebration though. Can't have him pulling that one in front of the family stand.\n\nCheers,\nDave\n"

        elif item == 11:
            Story['Sender'] = "Head Coach"
            Story['Subject'] = player['name']
            Story['Body'] = f"Hi {firstName},\n\n{player['name'].split()[0]} was struggling to keep up with today's training session. He's just got a new Instagram model girlfriend and I don't think he's getting his 8 hours sleep. You might need to ask him where his priorities lie.\n\nCheers,\nDave\n"
        
        elif item == 12:
            Story['Sender'] = "Secretary to the Chairman"
            Story['Subject'] = "Stationery"
            Story['Body'] = f"Hi {firstName},\n\nGlenn's lost his stapler again. I'm going to put it on a darn chain around his neck if it happens again.\nAnyway, I'm going to do another stationery order. Would you like anything?\n\nBest,\nMorag\n"

        elif item == 13:
            Story['Sender'] = "Secretary to the Chairman"
            Story['Subject'] = "Biscuits"
            Story['Body'] = f"Hi {firstName},\n\nI'm going to get some more biscuits in, but could we store them in your office going forward? Glenn can inhale an entire packet of chocolate hobnobs in a matter of minutes when left to his own devices.\n\nBest,\nMorag\n"

        elif item == 14:
            club = getRandomClub(userId)[0]
            Story['Club_id'] = club['club_id']
            Story['Sender'] = "Head Coach"
            Story['Subject'] = "Espionage"
            Story['Body'] = f"Hi {firstName},\n\nI'm sure that you've heard the news about {club['club_name']} antics, spying on their opponents. We are doing daily patrols around the perimeter of the training ground to keep an eye out for any suspicous activity. Glenn was toying with the idea of shipping in some 'trained' coyotes from one of his friends in Mexico, but I talked him out of it.\n\nCheers,\nDave\n"

        elif item == 15:
            Story['Sender'] = "The Chairman"
            Story['Subject'] = "Going Viral"
            Story['Body'] = f"Hi {firstName},\n\nI've just been doing some internet research and it seems that the kids are all about this 'TikTok'. I think that we should make a few videos. I read that some of these kids are making millions. MILLIONS!\n\nI have a few ideas already. Could you come and install it on my phone when you get a minute please {firstName}?\n\nWarm Regards,\nGlenn\n"
        
        elif item == 16:
            Story['Sender'] = "The Chairman"
            Story['Subject'] = "Board Meeting"
            if clubDict[0]['board_confidence'] > 90:
                Story['Body'] = f"Hi {firstName},\n\nThings are going so well at the minute I could kiss you! I am such a picture of zen that I've even stopped getting on the wife's nerves. Keep it up buddy!\n\nLove you,\nGlenn\n"
            elif clubDict[0]['board_confidence'] > 70:
                Story['Body'] = f"Hi {firstName},\n\nJust a quick message to let you how the board meeting went today. We're happy with how things are going generally. Of course, there's always room for improvement so keep chipping away and let me know if I can help with anything. Keep up the hard work.\n\nWarm Regards,\nGlenn\n"
            elif clubDict[0]['board_confidence'] > 50:
                Story['Body'] = f"Hi {firstName},\n\nSome of the guys on the board have been raising their concerns about your leadership. I'll keep fighting your corner but we're going to have to string some wins together soon champ.\nBig Glenn's here if you need to chat.\n\nRegards,\nGlenn\n"
            else:
                Story['Sender'] = "Secretary to the Chairman"
                Story['Body'] = f"Hi {firstName},\n\nGlenn was sobbing into a pile of hobnobs after the board meeting today. I don't think that you'll be getting a message from him but I think you should know that it didn't go well. We need to win some matches {firstName}. Do you want me to take training this week? You look like you need a break & to be honest, I think I'd do a better job.\n\nBest,\nMorag\n"

        elif item == 17:
            Story['Sender'] = "Secretary to the Chairman"
            Story['Subject'] = "Computer systems"
            Story['Body'] = f"Hi {firstName},\n\nHeads up that I've got the new intranet up and running now so things should run much more smoothly around here. I can't believe that it took 25 years for Glenn to concede that computers aren't just 'a fad'. Me and Dave are smashing up the filing cabinets this afternoon and I'm putting on a bit of a buffet to celebrate - feel free to join.\n\nBest\nMorag\n"

        elif item == 18:
            Story['Sender'] = "The Chairman"
            Story['Subject'] = "Building Work"
            Story['Body'] = f"Hi {firstName},\n\nExcuse the noise today. We've got some guys in to extend the trophy cabinet. No pressure or anything (but it will need filling). Lol, only joking (but really, it will).\n\nWarm Regards\nGlenn\n"

        elif item == 19:
            Story['Sender'] = "Head Coach"
            Story['Subject'] = "Today"
            Story['Body'] = f"Hi {firstName},\n\nHeads up - I'm running a bit late for training today gaffer. I stopped off at Sports Direct to get some new training cones and the traffic was mental in the city centre. £3 for 20 cones though so swings and roundabouts. See you soon.\n\nCheers\nDave\n"

        elif item == 20:
            club = getRandomClub(userId)[0]
            Story['Club_id'] = club['club_id']
            Story['Sender'] = f"Manager of {club['club_name']}"
            Story['Subject'] = "Catch Up"
            Story['Body'] = f"Hi {firstName},\n\nWe haven't been in touch much recently, just because we manage rival teams doesn't mean that we can't be friends. How about we go for a drink this weekend? I know a delightful wine bar where we won't be bothered by all the usual riff-raff. Say, 8pm? After Saturday's game. I promise not to get you too drunk and steal all of your secrets ; - )\n\nYours,\n{club['manager']}\n"
        
        elif item == 21:
            champions = getClubByPos(userId, 1)
            relegated = [getClubByPos(userId, 9), getClubByPos(userId, 10)]
            Story['Club_id'] = champions['club_id']
            if Story['Club_id'] != 20:
                Story['Sender'] = "Football Round Up"
                Story['Subject'] = f"{champions['club_name']} are champions!"
                Story['Body'] = f"{champions['club_name']} have been crowned the champions of English football after a hard fought season. The celebrations went on into the wee hours of the morning for {champions['manager']}'s team.\n\nThere was less to cheer about for {relegated[0]['club_name']} and {relegated[1]['club_name']}, as both clubs were relegated from the top league and will have to battle it out in the second tier next season.\n"
            else:
                Story['Sender'] = "The Chairman"
                Story['Subject'] = "We are the champions my friend!"
                Story['Body'] = f"I don't bloody believe it {firstName}! I have dreamt of this day but never thought it would come. Thank you so much!!!\n\nGet to my office ASAP - Morag's cracking out the champers.\n\nI love you, always,\n\nGlenn\n"
        
        elif item == 22:
            winner = getClubByPos(userId, 11)
            runnerup = getClubByPos(userId, 12)
            if winner['club_id'] == 20:
                winner = clubDict[0]
            if runnerup['club_id'] == 20:
                runnerup = clubDict[0]

            Story['Club_id'] = winner['club_id']
            Story['Sender'] = "Football Round Up"
            Story['Subject'] = f"{winner['club_name']} clinch the title"
            Story['Body'] = f"{winner['club_name']} will be mixing it with the big boys next season after finishing the season at the summit of the second tier. \n\n{runnerup['club_name']} ran them close and won't be too disappointed, as there 2nd place finish means that they'll join {winner['club_name']} at the top table of English Football.\n"
   
    return Story