:soccer: __C H A M P G A F F E R__ :soccer:
===========================================
_A web-based application using JavaScript, Python, Flask, and SQL_
------------------------------------------------------------------

_I N T R O_
-----------

__CHAMPGAFFER__ is a football (soccer) manager simulation game where the user is given the task of guiding their team out of the second-tier _Sub League_ (based on the English Championship) and onto glory in the _Super League_ (based on the English Premier League).  It was initially developed as a final project for Harvard's [CS50][] course.

The premise is built loosely around the early [Championship Manager][] games - with a fun, retro spin - using fictional teams and players with nods to the real world. The interface utilises [Bootstrap][] to enhance browser compatibilty and ensure a modern user-experience, but also offers hints of nostalgia with arcade fonts, Windows 98 inspired 'email', fixture lists and [Teletext][] matchday action, results and league standings.

The application uses a mixture of pre-determined and randomised elements to generate player/squad attributes and simulate results. Users can purchase players to improve their squad, increase the likelihood of winning matches, and work their way up the rankings.


_C H A M P G A F F E R . D B_
-----------------------------

The application is built around the `champgaffer.db`[SQLite][] database, consisting of the 8 data tables detailed briefly below:

+   _clubs_
    - stores the static details of each of the fictional clubs in the game
+   _club\_attr_
    - stores changable data for each club - unique to each user
+   _managers_
    - contains user details and keeps track of transfer budget and game number/season
+   _players_
    - stores the static details of each fictional player in the game
+   _player\_attr_
    - stores changeable data for each player - unique to each user
+   _fixtures_
    - contains/tracks the order/status of fixtures for the current season for each user
+   _news_
    - stores news items generated as mock emails in [news.py][] for each user
+   _goals_
    - tracks the no. of goals scored by each player throughout a season

The full data structure for the __CHAMPGAFFER__ database can be found in [schema.sql][]. 


_R A N D O M I S E R . P Y_
---------------------------

__CHAMPGAFFER__ uses various methods from _Python_'s [random][] module to randomise player and club attributes, namely _randint, choices, uniform and shuffle_. This randomiser magic mainly takes place in [randomiser.py][]. 

Each player's skill attributes are as follows, stored in `champgaffer.db`'s _player\_attr_ table, and are unique to each user/manager:

+   _Speed_
+   _Strength_
+   _Technique_
+   _Potential_
+   _Handsomeness_
+   _Ovr_  
+   _Age_
+   _Value_

_Speed_, _strength_, _technique_, _potential_ and _handsomeness_ are randomised with `random.choices`, weighted using the ratings of each player's starter club.

The _age_ attribute also uses `random.choices`, but is weighted separately, whilst _ovr_ is calculated using `statistics.mean`.

_Value_ (transfer cost) is computed using a mixture of key player attributes fed into weighted probabilities, added to an inital `random.randint`. Additional value is added to players whose _potential_ or _hansomeness_ attribute is greater than 17, or whose _handsomeness_ is 2 points greater than their _ovr_ rating:

[randomiser.py][]:
```python
if potential > 17:
    value += uniform(value * 0.1, value * 0.2)
if handsomeness > 17 or handsomeness > ovr + 2:
    value += uniform(value * 0.2, value * 0.4)
```

Along with the dynamic elements in the _player\_attr_ table, `champgaffer.db` is also seeded with some initial player data, stored in its _players_ table. Firstly, _nationality_ is determined from a weighted dictionary list of nations via `random.choices`. Each dictionary consists of a nationality, a nation code and the file name for a .svg file of the nation's flag, as follows:

[randomiser.py][]:
```python
nations = [
    {"nationality": "English", "nat_code": "en_GB", "flag": "eng.svg"}, 
    {"nationality": "Irish", "nat_code": "en_GB", "flag": "ire.svg"}, 
    {"nationality": "Scottish", "nat_code": "en_GB", "flag": "sco.svg"}, 
    {"nationality": "Welsh", "nat_code": "en_GB", "flag": "wal.svg"},
    ...
]
```

_nat\_code_ is passed into [Faker][]'s _Python_ package to seed the database with random first/last names, dependent on the selected nationality. _Faker_'s `first_romanized_name()` and `fake.last_romanized_name()` are used on any player/manager with a Japanese nationality code (`"ja_JP"`), and first and last names are concatenated accordingly:

[randomiser.py][]:
```python
def nameFaker(nat_code):
    fake = Faker(nat_code)
    if nat_code == "ja_JP":  
        name = fake.first_romanized_name() + " " + fake.last_romanized_name()
    else:
        name = fake.first_name_male() + " " + fake.last_name()
    return name
```

Initial club attributes are also seeded into the database via the `Teams` dictionary in [randomiser.py][] - a club's intial _ovr_ rating and manager name are randomised using `random.randint` and `Faker` respectively.

[randomiser.py][] is also home to a [round robin][] algorithm to schedule fixtures in a randomised manner that guarantees each team meeting twice in the 18 game season (home and away) - utilising `shuffle()` and `.reverse()`.

```python
def roundRobin(teams)
```


_G E N E R A T O R . P Y_
-------------------------

[generator.py][] contains various functions to seed the intial data in the _clubs_ and _players_ tables, as well as generating player attributes, club attributes, fixtures and news items unique to each user. This is often achieved by calling some of the aforementioned functions from [randomiser.py][]. 

`generatePlayerAttributes` and `generateClubAttributes` are called when a new user is entered into the `champgaffer.db` _managers_ table to populate the _player\_attr_ and _club\_attr_ tables with data unique to the user.

[generator.py][]:
```python
def generatePlayerAttributes(user, players)
```
. . .
```python
def generateClubAttributes(user, clubs)
```

`updatePlayerAttributes` is called at the start of each new season (discounting the first) and updates key fields in the _player\_attr_ table depending on a player's _age_ and _potential_ stats. 

```python
def updatePlayerAttributes(user)
```

`generateFixtures` is called at the start of every season and generates a randomised fixtures list for every club via the `roundRobin` function in [randomiser.py][], and stores them in `champgaffer.db`'s _fixtures_ table. 

```python
def generateFixtures(user, clubname, season)
```

Clubs are sorted in order of the _club\_attr_ table's _rank_ column, and `def roundRobin` is called twice to ensure match ups are limited to teams in the same league:

```python
    # generate fixtures for top league (10 highest ranked teams)
    premFixtures = roundRobin(clubList[:10])
```
. . .
```python
    # generate fixtures bottom league (10 lowest ranked teams)
    champFixtures = roundRobin(clubList[10:])
```

`def gotNews` handles the generation of specific or random news stories by entering the data pulled from calling `def getStory` in [news.py][] into `champgaffer.db`'s _news_ table. `gotNews` and `getStory` accept 3 arguments; _user\_id_, _news\_id_ and _player\_id_. Where a specific news story or player is required for the news item these can be plugged into the arguments accordingly. Otherwise, both _news\_id_ and _player\_id_ default to 0 and the news item and/or player are randomised:

[generator.py][]:
```python
def gotNews(user, news_id=0, pl_id=0)
```
. . .
[news.py][]:
```python
def getStory(user, news_id=0, pl_id=0)
```

_N E W S . P Y_
---------------

[news.py][] handles the generation of 22 dynamic news items formatted as emails that appear in a user's Windows '98 inspired 'Me-mail inbox'. The news items keep the user up to date with key game events including transfer offers, budgets, board expectations/confidence, league winners/runner-ups and relegations. These key news items are mixed with more humorous anecdotes regarding the club Chairman (Glenn), his secretary (Morag), the Head Coach (Dave), and players in the user's squad.

[news.py][]'s `getStory` function returns a dictionary with 7 key value pairs.

+   _Mail\_id_
    - which mail item is to be returned
    - randomly generated if unspecified in `getStory` argument
+   _Sender_
    - determined by _mail\_id_
    - changes dependent on _player\_id_, _mail\_id_ and _club\_id_
+   _Subject_
    - determined by _mail\_id_
    - changes dependent on _player\_id_, _mail\_id_ and _club\_id_
+   _Body_
    - determined by _mail\_id_
    - changes dependent on _player\_id_, _mail\_id_ and _club\_id_
+   _Player\_id_
    - which player (if any) the news story relates to
    - specified in `getStory` argument, or randomly generated
+   _Club\_id_
    - which club (if any) the news story relates to
    - randomly generated if required by _mail\_id_
+   _Offer_
    - the sum offered if the _mail\_id_ refers to a transfer offer
    - calculated using the [randomiser.py][] `playerValue` function and `random.uniform`


_M A T C H . P Y_
-----------------

[match.py][] deals with match set up and simulation with its two primary functions:

```python
def matchSetup(teamlineup, teamformation, teaminfo):
    """Return club and player stats to set up match"""
```

`matchSetup` compiles the data required for match simulation, returning a dictionary of team stats (`teamStats`), along with a dictionary list of player stats for each position/star players (`teamList`). Its 3 arguments consist of:

+   `teamLineup`
    - An ordered dictionary list of a team's selected players
+   `teamformation`
    - A string of a team's selected formation e.g. '4-4-2'
+   `teamInfo`
    - A dictionary containing club attributes pulled from `champgaffer.db`'s _clubs_ and _club\_attr_ tables

```python
def simMatch(homeStats, homeList, awayStats, awayList):
    """Simulate match using home and away stats"""
```

`simMatch` uses the team stats and line-ups to simulate a likely outcome for match up, taking into account each team's stats, home advantage and likely goalscorers - making use of averages, `random.randint` and `random.choices`. `simMatch` returns the following:

+   `glsHome` / `glsAway`
    - Simulated integers of goals scored by each team
+   `homeScorers` / `awayScorers`
    - Dictionary lists of home/away goalscorers and their stats
+   `attendance`
    - Integer of simulated match 'attendance' to display in gameplay

[match.py][]'s helper functions are self-explanatory: 

Called in `matchSetup` to return average player ratings:
```python
def posStats(posList):
    """Return avg ratings and star player for position"""
```

Called in `matchSetup` to determine star attacking player from best midfielder and best attacker:
```python
def getStarAtk(md, at):
    """Compare attacking star players"""
```

Called in `simMatch` to boost attendance in games where teams are 'rivals' or have similar league positions:
```python
def attendanceBoost(homestats, awaystats):
    """Boost attendances for rival matches"""
```

Refer to [match.py][] for full, commented algorithms.


_A P P . P Y_
-------------

[app.py][] pulls the whole shebang together taking care of the routing, template rendering and the majority of the database queries, insertions and updates. It is well commented, and its workings are referenced in the remainder of this document where related to specific pages.


_H T M L ,  C S S   &   L A Y O U T_
------------------------------------

The _HTML_ for the project is stored in the _/templates_ folder. Excluding the Teletext-inspired match simulation pages, each __CHAMPGAFFER__ page uses [Flask][] to extend [layout.html][]. The head of [layout.html][] contains links to global components of the app: 

+   The [main.css][] stylesheet, compiled using [less][] with imports of:
    - [Bootstrap][]'s _CSS_
    - [98.css][]: for Windows '98 styling
    - [teletext.css][]: for teletext styling
    - [styles.css][]: _CSS_ fine tuning
+   [jQuery][], [popper.js][] and [Bootstrap]'s _JavaScript_
+   [favicon.io][] favicons
+   [font awesome][] icons

[layout.html][] also handles the global [Bootstrap][] navigation bar, positioning of [flash messages][] and acknowledgements in the footer. Here also lives the simple loading page, which appends an animated loader icon to a pre-loaded page and removes it once all elements have loaded to the DOM. A [setTimeout()][] fallback is included in the event of a page item failing to load after 5 seconds:

[layout.html][]
```javascript
$(window).on('load', function(){
    removeLoader(); //wait for page load
});
window.setTimeout(removeLoader, 5000); // fallback if some content fails to load
```

Layout and content alignment for all non-Teletext pages is handled by _Bootstrap_'s [grid system][], ensuring responsiveness and flexibilty in the page layouts.

All _CSS_ and image files can be found in the [static][] folder. The majority of the application's _JavaScript_ is page specific and can therefore be located in the body of the relevant page's _HTML_. Additional _JavaScript_ files are stored in [static/js][].


_S I G N U P   &   L O G  I N_
------------------------------

In order to play __CHAMPGAFFER__, a user must first sign-up to enter their team/manager details into the `champgaffer.db` [SQLite][] database and login. Log ins are determined via the `@login_required` decorated function located in [helpers.py][]. If a user isn't logged in, they are redirected to the _/login_ route to log in or sign up:

[helpers.py][]:
```python
# check for log in
def login_required(f):
@wraps(f)
def decorated_function(*args, **kwargs):
    if session.get("id") is None:
        return redirect("/login")
    return f(*args, **kwargs)
return decorated_function
```

The _/signup_ page consists of a 6-field form with multiple levels of validation, requiring:

+   Username
+   Manager name
+   Club name
+   Password
+   Confirm password

All fields are validated using _Bootstrap's_ [form-control][] classes, along with the _HTML_ `required` field. It is also mandatory that the _Username_ and _Club name_ fields are unique to avoid data collisions. This is ensured with database queries once the form is passed. _Flask_ [flash messages][] are passed to communicate any invalid submissions:

[app.py][]:
```python
# check username is valid (has been entered and isn't already in database)
username = request.form.get("username").lower()
if not username or db.execute("SELECT * FROM managers WHERE username = ?", username):
    flash('Username is invalid or already in use.', 'alert-danger')
    return redirect("/signup")

# check club name is valid (has been entered and isn't already in database)
clubname = request.form.get("clubname")
if not clubname or db.execute("SELECT * FROM managers WHERE club_name = ?", clubname):
    flash('Club name is invalid or already in use.', 'alert-danger')
    return redirect("/signup")
```

If a sign up is successful, the user's details are entered into `champgaffer.db`'s _managers_ table - the _Password_ field is hashed using _werkzeug.security_'s [generate_password_hash][] method -
and player attributes and club fixtures are generated.

The _/login_ page is a condensed version of the sign-up form, requiring only a previously signed up user's _Username_ and _Password_. Population and validity of fields is again determined via _Bootstrap_ and _HTML_. If the _Username_ and _Password hash_ (checked with `check_password_hash`) match, _id_ is stored with [Flask-Session][], and the user is redirected to the _/_ route: 

[app.py][]:
```python
# Query database for username
rows = db.execute("SELECT * FROM managers WHERE username = :username",
                    username=request.form.get("username").lower())

# Ensure username exists and password is correct
if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
    flash('Your password and/or username were entered incorrectly.', 'alert-danger')
    return render_template("login.html")

# Remember which user has logged in
session["id"] = rows[0]["id"]
```
. . .
```python
# Redirect user to home page
return redirect("/")
```


_I N D E X  /  C L U B  P A G E S_
----------------------------------

[index.html][] acts as an 'office' for the manager - using Flask-injected _HTML_ to display manager 'emails', along with squad details, star players, upcoming club fixtures, remaining budget and board confidence.

The Windows '98 inspired email and fixture list page elements are adapted from [98.css][]. The fixture window displays the user's upcoming fixtures, while the email window provides the user with access to their 10 most recent news items. To give the email UI an authentic flavour, the body of an email is viewable via a customised _Bootstrap_ [modal][]. New emails display in bold with an 'unread' icon, and the content of the news item is passed into the modal on click. Unread items are determined by a boolean in the _read_ column of the `champgaffer.db` _news_ table, which defaults to 0 (false) when a news item is generated.

Emails are dynamically marked as 'read' without reloading the page using a form passed to the `/read` route in an [Ajax][] request - sent on opening the news modal. If the request is successful, the `champgaffer.db` _news_ table's _read_ column is set to 1 (true), the unread icon is switched out and font weight set to normal:

[index.html]:
```javascript
$('#newsModal').on('show.bs.modal', function (event) {
            if (read == 0) {
```
. . .
```javascript
$.ajax({
    url : "/read",
    data : $('#read').serialize(),
    type : 'POST',
    success: function(response) {
        console.log(response);
        read = 1;
        document.getElementById(`ricon${obj['news_id']}`).innerHTML = "<i class='far fa-envelope-open'>";
        document.getElementById(`eRow${obj['news_id']}`).style.fontWeight = "normal";
```

Player cards are styled loosely on 80s/90s Panini [football stickers][], using [DiceBear][] generated avatars, nation flags, team colours and player statistics pulled from the `champgaffer.db` _player\_attr_ table. The manager card and star player cards are included in the flow of the [index.html][] and [club.html][] pages. Player cards for squad players can also be viewed as _Bootstrap_ [modal][] windows accessed through clickable rows in the squad list tables.

[club.html][] is a stripped back version of [index.html][], which provides dynamic information for each club in the user's universe. Emails and fixtures are ommitted, but club/manager stats, star players and squad lists (including player card modals) are all viewable.

The dynamic club pages are accessible through Javascript constructed URLs when clicking a club's name in the _standings_, _stats_ and _matchday_ pages - or in a player modal:

[clubs.html][]:
```javascript
var club_link = club['club_name'].replace(" ", "_")
```

The club routes are handled in [app.py][]'s `profile` function, querying `champgaffer.db` for the relevant club info:

[app.py][]
```python
@app.route("/<club_name>")
@login_required
def profile(club_name):
    """Display club info"""

    # identify club
    session['clubInfo'] = db.execute("SELECT * FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE (club_name = ? AND club_attr.manager_id = ?) AND clubs.club_id < 20;",
                      club_name.replace("_", " "), session['id'])
```


_T R A N S F E R S_
-------------------

Player transfers are primarily carried out by manager searches on __CHAMPGAFFER__'s `/transfers` page. The route's _GET_ method renders [transfers.html][] to display a table of all game players except those in the user's own squad - comprising of rival club players and free agents. This list can be easily filtered to a user's requirements using the search form powered by the route's _POST_ method. Validation isn't required as the database query triggered by the form overlooks any blank fields. The search form consists of the following fields:

+   _Player name_
    - text field for specific player searches
    - utilises SQLite's `LIKE` [operator][] for partial matches
+   _Club_ 
    - drop down list of clubs (defaults to 'All Clubs')
    - displays only players in a certain team
+   _Postition_ 
    - drop down list of player positions (defaults to 'All positions')
    - displays only players in a certain position
+   _Ovr_
    - number field with min value of 1 and max value of 20
    - utilises SQLite's `>=` [operator][] to select only players above or equal to specified value
    - submitted to query as 1 if field is left blank
+   _Max Value_
    - drop down list of maximum player values (defaults to 40)
    - utilises SQLite's `<=` [operator][] to select only players below or equal specified value

As with the [index.html][] and [club.html][] pages, table rows are clickable to access more details on a player. Clicking a row triggers a _Bootstrap_ [modal][] window displaying the relevant player's player card. All of the neccesary data for the player card is again passed into the [modal][] on its opening and displayed with _jQuery_. A hidden form is also populated with the relevant player's data on the opening of a player card [modal][] using _JavaScript_:

[transfers.html][]:
```html
<form action="/buy" id="buyform" method="post" style="display: none;">
    <input name="pl_id" id="pl_id">
    <input name="cl_id" id="cl_id">
    <input name="cl_name" id="cl_name">
    <input name="cl_rank" id="cl_rank">
    <input name="pl_cost" id="pl_cost">
    <input name="pl_pos" id="pl_pos">
    <input name="squad_num" id="squad_num">
</form>
```
. . .
```javascript
$('#playerModal').on('show.bs.modal', function (event) {
    var player = $(event.relatedTarget)
    var deets = player.data('player').replace(/['']+/g, '"');
    deets = JSON.parse(deets);
```
. . .
```javascript
document.getElementsByName("pl_id")[0].value = deets['player_id'];
document.getElementsByName("cl_id")[0].value = deets['club_id'];
document.getElementsByName("cl_name")[0].value = deets['club_name'];
document.getElementsByName("cl_rank")[0].value = deets['rank'];
document.getElementsByName("pl_cost")[0].value = deets['cost'];
document.getElementsByName("pl_pos")[0].value = deets['pos'];
document.getElementsByName("squad_num")[0].value = deets['squad_num'];
```

From here, the user can click through to a club page, close the window to keep browsing, or hit _'Buy Player'_ to place an offer for the player. Where _'Buy Player'_ is clicked, a confirmation message is fired before submitting the form for a more flexible user experience:

[transfers.html][]
```javascript
// Unbind any previously cancelled events and fire confirmation message
$(document).off('click', '#buy').on('click', '#buy', function (event) {
    if (!confirm(msg)) {
        return false;
    }
    else {
        form.submit();
        return true;
    }
});
```

Player sales are carried out in a similar fashion (using hidden forms and modal data), but these events are triggered by randomised transfer offer 'emails' periodically sent to a user's mock inbox on the homepage. A manager has the option to accept or reject transfer offers for their players as they arise. The user can also opt to 'release' a player via their player card modal in the squad list. 

The buying and selling of players is handled via _POST_ methods in the `/buy` and `/sell` routes of [app.py][].

[app.py][]
```python
@app.route("/buy", methods=["POST"])
@login_required
def buy():
```
. . .
```python
@app.route("/sell", methods=["POST"])
@login_required
def sell():
```

The `/buy` route uses data retrieved from the player purchase form to determine the viability of a transfer, displaying `'alert-danger'` [flash messages][] and generating news items to communicate if a transfer is unsuccessful:

[app.py][]:
```python
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
        # construct rejection email and display flash message
        gotNews(session['id'], 3, session['pl_id'])
        flash(f"It doesn\'t look like that player is interested - check your emails for details.", 'alert-danger')
        return redirect('/transfers')
```

In the case of a successful transfer, an important check is to make sure that a selling team's squad doesn't contain fewer than 11 players. If this is the case, a new player is generated to replace them:

[app.py][]:
```python
# if user has funds and offer accepted generate new player for selling club (if not a free agent & squad < 11)
session['playerCount'] = db.execute("SELECT count(*) FROM player_attr WHERE club_id = ? AND manager_id = ?;", 
                                    session["cl_id"], session["id"])[0]
if session["cl_id"] != 21:
    if session['playerCount']['count(*)'] < 12:
        session["newPlayer"] = makePlayer(session["pl_pos"], session["squad_num"], session["cl_name"])
        session["pl_stats"] = makeAttr(session["cl_name"])
```

The remaining steps of a successful transfer complete updates to the user budget and player squad number and generates the relevant news emails from [news.py][]. Finally, the user is redirected to their homescreen and an `'alert-success'` [flash message][] is displayed to indicate success and inform them of their remaining budget:

[app.py][]:
```python
#  redirect to office page and display success message confirming transfer
flash('Purchase successful. Your updated transfer budget is £' + str(session["newBudget"]) + 'm.',
        'alert-success')
return redirect('/')
```

The `/sell` route uses data retrieved from a player sale/release form to determine the viability of a transfer or player release. There are less conditions to cater for in the case of a sale - the only check needed to pass is ensuring that the user's squad is large enough for the sale/release to go through. If this is the case an `'alert-danger'` _flash message_ informs the user:

[app.py][]:
```python
# query database for user club details and squad size
session["userClub"] = db.execute("SELECT * FROM managers JOIN club_attr ON managers.club_id = club_attr.club_id WHERE id = ?;",
                                 session["id"])[0]

session['playerCount'] = db.execute("SELECT count(*) FROM player_attr WHERE club_id = 20 AND manager_id = ?;", 
                                    session["id"])[0]['count(*)']

if session['playerCount'] < 11:
    #  squad too small - redirect to office page and display error message
    flash(f"Sorry, we don't have a big enough sqaud to let that player go - Glenn.", 'alert-danger')
    return redirect('/')
```

If a sale is successful, budgets and _club\_id_ attributes are updated accordingly and a new, random news item is called. The user is redirected to the `/` route, and a relevant `alert-success` _flash message_ is constructed and displayed:

[app.py][]:
```python
#  redirect to office page and display success message confirming player release/sale
if session["cl_id"] == 21:
    flash('Player released. Your updated transfer budget is £' + str(session["newBudget"]) + 'm.', 'alert-success')
else:
    flash('Player sold to ' + session['cl_name'] + '. Your updated transfer budget is £' + str(session["newBudget"]) + 'm.', 'alert-success')

return redirect('/')
```


_S T A N D I N G S_
-----------------------------

The `/standings` route queries `champgaffer.db` for the data required to calculate current league standings before rendering [standings.html][]. `ORDER BY` sorts the teams into their relevant league positions using `pts` and `gd` ([goal difference][]) columns:

```python
@app.route("/standings", methods=["GET"])
@login_required
def standings():
    """Display current standings"""

    session["getStandings"] = db.execute("SELECT club_name, rank, pld, gs, ga, (gs - ga) AS gd, pts, pos, pos_track FROM club_attr JOIN clubs on club_attr.club_id = clubs.club_id WHERE manager_id = ? AND rank < 21 ORDER BY pts DESC, gd DESC, pos ASC;", session["id"])
```

_Python_ `for` loops and `if else` statements, inserted using _Flask_ [Jinja][] templating, ensure that teams are displayed in their relevant leagues, and determines styling for teams in promotion/relegation zones and which team progress icon to display:

[standings.html][]:
``` python
{% if club['pos'] < club['pos_track'] %}
    {% set arrow = "fa-caret-up" %}
{% elif club['pos'] == club['pos_track'] %}
    {% set arrow = "fa-minus" %}
{% else %}
    {% set arrow = "fa-caret-down" %}
{% endif %}
{% if club['pos'] == 1 %}
    {% set class = "borderup promotion" %}
{% elif club['pos'] == 8 %}
    {% set class = "borderdown" %}
{% elif club['pos'] > 8 %}
    {% set class = "relegation" %}
{% else %}
    {% set class = "" %}
{% endif %}
```


_S T A T S_
-----------

The `/stats` route queries `champgaffer.db` for the data required to calculate current top scorers for each league before rendering [stats.html][]. It is also possible to access a player's [modal][] card and make transfer offers through the same mechanisms as [transfers.html], index and club pages.


_M A T C H D A Y_
-----------------

The `/matchday` route in [app.py][] is where the setup for user matches takes place. The user is presented with a list of their squad and possible formations, next to their opponents starting 11 and formation. This is acheived through `champgaffer.db` queries to return the relevant user and opponent data before rendering the [matchday.html][] page. The page also makes heavy use of _JavaScript_, _jQuery_ and _HTML_'s [drag and drop][] API for user interfacing and form construction. 

Numerous interfaces were considered for user submission of their starting line-up, but drag and drop felt like the most intuitive - as well as allowing squads to be displayed in the table format that is familiar from other pages of the application. When a user is happy with the line-up that they have chosen, the _Update Lineup_ button is clicked, firing the `update()` function. This function uses _JavaScript_ to push the data of each player in their chosen order to two separate arrays:

+   `starters`
    - stores only the 11 players selected by the user to start the game
    - required for match simulation
+   `squad`
    - stores the whole of squad in order
    - required to remember order of selection and update squad numbers

[matchday.html][]:
```javascript
if (starters.length < 11) {
    starters.push(curPlayer);
    squad.push(curPlayer);
}
else {
    squad.push(curPlayer)
}
```

`update()` also uses a sprinkling of _jQuery_ to add the selected player's avatars/names to the page in the selected team formation without requiring a page reload:

[matchday.html][]:
```javascript
var count = 10;
$('.plImg').each(function (){
    $(this).attr("src",`https://avatars.dicebear.com/v2/male/${starters[count]['name']}.svg`);
    $(this).next().text(`${count + 1}: ${starters[count]['name']}`);
count--;
})
```

The user can choose from 5 classic football formations for their team, displayed on the page using _CSS_ [flex][], combined with _CSS_'s [grid column][] property. The [grid column][] `span` syntax, combined with _JavaScript_ helps to reposition players neatly in their container, with [flex][] ensuring that the dynamic content stays neatly centered and aligned. This concept borrows heavily from [Hannah Oppenheimer][]'s approach to displaying footabll formations.

For separation, the _JavaScript_ for [drag and drop][] functionality and formation changes is kept in [lineup.js][] and [formation.js][] respectively.

Once the user has selected their team and formation, the _Proceed_ button will populate a hidden _HTML_ form with player/formation data, using the `toMatch()` _JavaScript_ function. This form is delivered via the _POST_ method to the `/match` route ready for the match to be simulated.


_T E L E T E X T   P A G E S_
-----------------------------

__CHAMPGAFFER__'s match simulation pages are deliberately styled very differently to other routes in the application to make match action distinctive events in the game's flow. The styling of these pages recreate football [Ceefax][] pages - the BBC's [Teletext][] service that ran from 1974 to 2012 - providing a sense of nostalgia to anybody familiar with checking the sports results on the service 'back in the day' (& a WTF moment for anybody else). 

Resultantly, these pages don't pull from [layout.html][] and don't use any _Bootstrap_ _CSS/JavaScript_- relying instead on the [teletext.css][] stylesheet and inline _JavaScript_. The foundations of [teletext.css][] were gratefully adapted from the wonderful [GALAX teletext][] font/CSS.

Although the [GALAX teletext][] _CSS_ was extrememly useful in getting started with the colours, fonts and concepts for the match screens - much more flexibility and variation was required for the pages to work with dynamic content on different screen sizes. This is achieved primarily with the use of _CSS_ [flex][] columns and [@media screen][] breakpoints.

The [teletext.css] styling is used in the gameflow on 3 consecutive _Flask_-injected _HTML_ pages:

+   [match.html][]
    - user match simulation page
+   [results.html][]
    - displays simulated results of all teams
+   [teletable.html][]
    - displays updated league tables in teletext form


_M A T C H . H T M L_
---------------------

The `/match` route is where user match action is simulated through a combination of _JavaScript_ and _Flask_-injected data via functions called from [match.py][]:

[app.py][]
```python
@app.route("/match", methods=["GET", "POST"])
@login_required
def match():
    """Simulate match"""
```

The route's `POST` method in [app.py][] receives the form submitted from [matchday.html], and uses this data to store home and away variables required by [match.py][]'s `matchSetup` and `simMatch` functions. The order of the team submitted by the manager is also submitted to the `champgaffer.db` at this point using the _squad\_num_ column in the _player\_attr_ table - ensuring that the user's team selection is remembered for the next match:

[app.py][]:
```python
squadnum = 1
for player in session["userSquad"]:
    db.execute("UPDATE player_attr SET squad_num = ? WHERE player_id = ? AND manager_id = ?;",
    squadnum, player["player_id"], session['id'])
    squadnum += 1
```

The outcomes of the `simMatch` function are used to determine the points won by each team, before updating the `champgaffer.db` _club\_attr_, _fixtures_ and _goals_ tables with the new data:

[app.py][]:
```python
if session['homeGls'] > session['awayGls']:
    homePts = 3
    awayPts = 0
elif session['awayGls'] > session['homeGls']:
    homePts = 0
    awayPts = 3
else:
    homePts = 1
    awayPts = 1
```

Board confidence is also updated for the user in `champgaffer.db` _managers_ table, dependent on the result - a win or draw increases board confidence (up to a maximum of 100), whilst a loss decreases board confidence (minimum of 0). Finally, [match.html][] is rendered with relevant data for the match 'kick-off'.

Whilst the score/scorers is pre-determined by [app.py][]'s call to `simMatch` from [match.py][], the order and timing of the goals is randomised by _JavaScript_ once [match.html][] is loaded to the DOM. Firstly, the scorers for each team passed into the DOM via _Flask_ are added to a separate _JavaScript_ arrays:

[match.html][]:
```javascript
// add home scorers to array
for (let i = 0; i < home.length; i++) {
    homeGls.push(home[i].name)
}
// add away scorers to array
for (let i = 0; i < away.length; i++) {
    awayGls.push(away[i].name)
}
```

Next, using a decrementing while loop, goals are added to `homeScorers` and `awayScorers` arrays as subarrays to be displayed to the user later. The subarrays consist of a goalscorer's name and a minute randomly generated by a `getRandomInt(min, max)` function, along with the `getMinutes(mins, ft)` function (called by the `goal(teamGls, mins, ft)` function) - which ensures that goals are saved to the subarrays in order, and spaced out realistically across the game.

[match.html][]:
```javascript
goalsTtl = homeGls.length + awayGls.length
homeScorers = []
awayScorers = []
added = getRandomInt(1,7);
ft = getRandomInt(90,90 + added)
ht = 45;
mins = 0;

while (goalsTtl > 0) {
    ha = getRandomInt(0,1)
    if (ha == 1 && homeGls.length > 0) {
        gl = goal(homeGls, mins, ft)
        gs = gl[1]
        mins = gl[0]
        homeGls = removeItem(homeGls, gs)
        homeScorers.push(gl)
        goalsTtl--;
    }
    if (ha == 0 && awayGls.length > 0) {
        gl = goal(awayGls, mins, ft)
        gs = gl[1]
        mins = gl[0]
        awayGls = removeItem(awayGls, gs)
        awayScorers.push(gl)
        goalsTtl--; 
    }
}
```

The `removeItem(arr, value)` function called here ensures that the same goalscorers passed into the DOM by _Flask_ are not repeated unduly, by being removed from the intially constructed `homeGls` / `awayGls` arrays as they are added into the corresponding `homeScorers` / `awayScorers` subarrays.

[match.py][]:
```javascript
function removeItem(arr, value) { 
            var index = arr.indexOf(value);
            if (index > -1) {
                arr.splice(index, 1);
            }
            return arr;
        }
```

Now that the details of the goals/goalscorers are safely stored in the scorers arrays, the user can click the [match.html][]'s _Kick Off_ button and the exciting bits can happen. The click triggers the `kickOff()` _JavaScript_ [async function][] which updates page content as the game progresses. The match timer increments every 100ms using a call to a `sleep(ms)` function utilising a _JavaScript_ [Promise][] and [setTimeout()] function:

[match.html][]:
```javascript
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

Using [setInterval()][] was initially trialled for triggering changes in the page content during match simulations, but the `sleep(ms)` function was much more flexible for the varied nature of match events.

`kickOff()` compares a `counter` variable to the minute of each goal scored by combining a `while` loop running until half-time/full-time with inner `for` loops, updating the page content using the `reportGoal()` async function. `await sleep()` effectively pauses the counter's incrementation until the animations are completed and the scoreline is updated:

[match.html][]
`kickOff()`:
```javascript
for (let i = 0; i < homeScorers.length; i++) {
    if (counter === homeScorers[i][0]) {
        hg++;
        reportGoal("home", homeScorers[i], hg, ag);
        await sleep(2900);
        document.querySelector('#score').textContent=`${hg} - ${ag}`
    }
}
```

`reportGoal()` triggers _JavaScript_ animations, firstly with a blinking effect creating by changing the text content and repeatedly inverting the colour of the `#score` element. 

[match.html][]
```javascript
async function reportGoal(team, teamScorer, hg, ag)
```
. . .
```javascript
    locateScore.textContent = "GOAL!!!"
    while (flash < 30) {
        
        if (flash <= 8) {
            if (locateScore.style.color == 'white') {
                locateScore.style.color = 'black';
            }
            else {
                locateScore.style.color = 'white';
            }
        }
```

Once this part of the animation is completed, a call to `goalText()` reveals the previously hidden `#pundit` element, with text content determined by `if else` providing the user with details on the goal, whilst `displayGoal()` creates a new page element containing the goal scorer/minute and appends to the page:

[match.html][]
```javascript
function goalText(team, teamScorer, hg, ag)
```
. . .
```javascript
string = `It's in! ${teamScorer} puts ${homeTeam} ahead.`;
```

``` javascript 
function displayGoal(team, minute, scorer) {
    var newP = document.createElement("p");
    var content = document.createTextNode(`${scorer}, ${minute}`);
    var addHere, parentDiv;

    if (team == "home") {
        addHere = document.getElementById('home');
    }
    else {
        addHere = document.getElementById('away');
    }

    newP.appendChild(content);
    parentDiv = addHere.parentNode
    parentDiv.insertBefore(newP, addHere);
}
```
This process is repeated until all goals have been displayed, and `counter` is equal to the `ft` (full-time) variable. At this point, the _Proceed_ button previously styled to `display: none` is revealed - linking to the `/results` route of the application. 


_R E S U L T S . H T M L   /   T E L E T A B L E . H T M L_
-----------------------------------------------------------

The `/results` route render the [results.html][] teletext page, presenting the user with all results for the current match day fixtures, as generated by calls to [match.py][]'s `simMatch`. `/teletable` displays league standings queried from `champgaffer.db`'s updated _club\_attr_ table.

Results and standings for each of the two leagues are separated by emulating teletext's automatically rotating pages - achieved using _JavaScript_ and [setInterval()][]: 

```javascript
function isVisible(elem) {
    return elem.offsetWidth > 0 || elem.offsetHeight > 0;
}
setInterval(function(){
    var sub = document.querySelector("#subLeague");
    var sup = document.querySelector("#superLeague");
    if(isVisible(sub)) {
    sub.style.display = 'none';
    sup.style.display = 'block'
    } else {
    sup.style.display = 'none';
    sub.style.display = 'block'
    }
},10000);
```


_F U T U R E   C O N S I D E R A T I O N S_
-------------------------------------------

Due to the considerable size of its undertaking, __CHAMPGAFFER__ was developed with a _'make it work and move forward'_ approach. Resultantly, there are surely enhancements to be made to the performance and, in some cases, the succinctness of the code. Improvements on both of these counts could be made when moving the app into production.

_JavaScript_ and _jQuery_ was at times used interchangeably as a learning exercise, but _JavaScript_ is increasingly versatile and would be favoured during any reconfiguration of the app's _HTML_.

[SQLite][] was the obvious choice for the database engine during development as it had been heavily introduced in the [CS50][] lectures and problem sets. A familiarity with its syntax was essential for the initial structure and planning of the application's data relationships. However, using [SQLite][] in production [tends not to be scaleable][].

Migrating data into [PostgreSQL][] from [SQLite][] is advisable for moving __CHAMPGAFFER__ into production, possibly making use of [pgloader][]. Initial trialling suggests that migrating data from [SQLite] is often [less straightforward][] for databases requiring the transfer of existing data, as is the case with __CHAMPGAFFER__. For future projects, using [PostgreSQL]][] or similar during the development phase could be favoured for a more seamless transfer into production.

The testing of __CHAMPGAFFER__'s main processes were fairly extensive during work on the project. Any major bugs discovered have been removed - but more intensive manual and automated testing is recommended before scaling the application. The front-end should be fairly stable across most screen sizes and browsers with its heavy reliance on [Bootstrap][]. All pages has been trialled substantially on _Chrome_ and _Safari_ on desktop, but significant testing on other browsers and mobile devices is required. In particular, the use of _HTML_'s [drag and drop][] API in [matchday.html][] needs [some consideration][] for transferability to mobile browsers.


[CS50]: https://cs50.harvard.edu/     "Link to Harvard's CS50 course"
[Championship Manager]: https://en.wikipedia.org/wiki/Championship_Manager      "Championship Manager Wikipedia page"
[Bootstrap]: https://getbootstrap.com/      "Bootstrap site"
[Teletext]: https://en.wikipedia.org/wiki/Teletext      "Teletext Wikipedia page"
[SQLite]: https://www.sqlite.org/index.html     "SQLite site"
[news.py]: news.py        "This file handles the generation of news emails"
[schema.sql]: schema.sql       "Champgaffer data tables"
[random]: https://docs.python.org/3/library/random.html     "Python random docs"
[Faker]: https://faker.readthedocs.io/en/master/        "Python Faker docs"
[randomiser.py]: randomiser.py     "This file handles player/fixture randomising"
[round robin]: https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm        "Round robin scheduling on Wikipedia"
[generator.py]: generator.py    "This file handles the generation of various game attributes unique to each user"
[match.py]: match.py      "This file handles the simulation of matches"
[app.py]: app.py        "Main application file for Champgaffer"
[Flask]: https://flask.palletsprojects.com/en/1.1.x/    "Flask docs"
[layout.html]:  templates/layout.html       "HTML file for common page layout"
[main.css]: static/css/main.css       "less compiled, main.css stylesheet"
[less]: http://lesscss.org/     "Less"
[98.css]: https://jdan.github.io/98.css/    "Adapted for the 'Windowfied' elements of the app"
[teletext.css]: static/css/teletext.css     "CSS for Teletext pages"
[styles.css]: static/css/styles.css     "Stylesheet for general customisations"
[jQuery]: https://jquery.com/       "jQuery site"
[flash messages]: https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/     "Flask message flashing docs"
[setTimeout()]: https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setTimeout       "JavaScript setTimeout() Mozilla docs"
[popper.js]: https://popper.js.org/     "popper.js (tooltip and popover positioning) site"
[grid system]: https://getbootstrap.com/docs/4.5/layout/grid/       "Bootstrap grid system docs"
[static]: static/       "Champgaffer static folder (CSS, images, fonts and JavaScript)"
[static/js]: static/js       "Champgaffer JavaScript folder"
[helpers.py]: helpers.py        "Helper functions"
[form-control]: https://getbootstrap.com/docs/4.0/components/forms/#form-controls       "Bootstrap form-control docs"
[generate_password_hash]: https://werkzeug.palletsprojects.com/en/1.0.x/utils/      "Werkzeug utilities documentation"
[Flask-Session]: https://pypi.org/project/Flask-Session/    "Flask-Session docs"
[index.html]: templates/index.html      "Flask injected HTML file for index page"
[modal]: https://getbootstrap.com/docs/4.5/components/modal/        "Bootstrap modal docs"
[Ajax]: https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX     "MDN Ajax docs"
[football stickers]: https://www.theguardian.com/sport/gallery/2013/may/15/beautiful-games-old-panini-stickers-gallery        "Guardian old school Panini"
[DiceBear]: https://avatars.dicebear.com/       "DiceBear avatars docs"
[club.html]: templates/club.html        "HTML for dynamic club profile pages"
[transfers.html]: templates/transfers.html        "HTML for transfer page"  
[operator]: https://www.sqlite.org/lang_expr.html   "SQLite language expressions docs"
[standings.html]: templates/standings.html      "HTML for league standings page"
[goal difference]: https://en.wikipedia.org/wiki/Goal_difference        "Wikipedia for goal difference"
[Jinja]: https://jinja.palletsprojects.com/en/2.11.x/       "Jinja docs"
[stats.html]: templates/stats.html        "HTML for stats page"
[matchday.html]: templates/matchday.html        "HTML for match set up page"
[drag and drop]: https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API        "HTML Drag and Drop API Mozilla docs"
[flex]: https://developer.mozilla.org/en-US/docs/Web/CSS/flex        "CSS flex docs"
[Hannah Oppenheimer]: https://www.opihana.com/2017/11/08/Soccer-Formations-in-CSS-Grid/     "The execution of my football formation layouts were based heavily on this CSS Grid concept"
[lineup.js]: static/js/lineup.js        "JavaScript file for flexbox driven formation changes"
[formation.js]: static/js/formation.js     "JavaScript file for handling drag and drop line-ups"
[Ceefax]: https://www.bbc.co.uk/sport/football/29242558       "BBC article detailing some history on their Ceefax service"
[GALAX teletext]: https://galax.xyz/TELETEXT/       "GALAX teletext font/CSS"
[@media screen]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media        "CSS @media Mozilla docs"
[match.html]: templates/match.html      "HTML for match simulation 'teletext' page"
[results.html]: templates/results.html      "HTML for simulated results 'teletext' page"
[teletable.html]: templates/teletable.html      "HTML for 'teletext' league standings page"
[async function]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function        "JavaScript async function Mozilla docs"
[Promise]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise     "JavaScript Promise Mozilla docs"
[setTimeout()]: https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setTimeout      "Mozilla setTimeout() docs"
[setInterval()]: https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setInterval     "Mozilla setInterval() docs"
[tends not to be scaleable]: https://djangodeployment.com/2016/12/23/which-database-should-i-use-on-production/     "Discussion on production phase of web applications using relational databases"
[PostgreSQL]: https://www.postgresql.org/docs/      "PostgreSQL docs"
[pgloader]: https://pgloader.readthedocs.io/en/latest/ref/sqlite.html       "pgloader docs"
[less straightforward]: https://medium.com/@anyazhang/publishing-a-flask-web-app-from-the-cs50-ide-to-heroku-osx-e00a45338c14       "Medium blog on pusblishing Flask app to Heroku"
[some consideration]: https://medium.com/@deepakkadarivel/drag-and-drop-dnd-for-mobile-browsers-fc9bcd1ad3c5        "Medium blog on Drag and Drop for mobile browsers"

