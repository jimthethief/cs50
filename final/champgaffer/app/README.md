__C H A M P G A F F E R__
=========================
_A web-based application using JavaScript, Python, Flask, and SQL_
------------------------------------------------------------------

_I N T R O_
-----------

__CHAMPGAFFER__ is a football (soccer) manager simulation game where the user is given the task of guiding their team out of the second-tier _Sub League_ (based on the English Championship) and onto glory in the _Super League_ (based on the English Premier League).

The premise is built loosely around the early [Championship Manager][] games - with a fun, retro spin - using fictional teams with nods to the real world. The interface utilises [Bootstrap][] to enhance browser compatibilty and ensure a modern user-experience, but also offers hints of nostalgia with arcade fonts, Windows 98 inspired 'email', fixture lists and [Teletext][] matchday action, results and league standings.

The game uses a mixture of pre-determined and randomised elements to generate player/squad attributes and simulate results. Users can purchase players to improve their squad, increase the likelihood of winning matches, and work their way up the rankings.

_S I G N U P  &  L O G  I N_
-----------------------------

In order to play __CHAMPGAFFER__, a user must first sign-up to enter their team/manager details into the `champgaffer.db` [SQLite][] database and login. Log ins are determined via the `@login_required` decorated function located in `helpers.py`. If a user isn't logged in, they are redirected to the _/login_ route to log in or sign up:

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

_C H A M P G A F F E R . D B_
-----------------------------

The `champgaffer.db` _SQLite_ database consists of 8 data tables, detailed briefly below:

+   _clubs_: stores the static details of each of the fictional clubs in the game
+   _club\_attr_: stores changable data for each club - unique to each user
+   _managers_: contains user details and keeps track of transfer budget and game number/season
+   _players_: stores the static details of each fictional player in the game
+   _player\_attr_: stores changeable data for each player - unique to each user
+   _fixtures_: contains/tracks the order/status of fixtures for the current season for each user
+   _news_: stores news items generated as mock emails in [news.py][] for each user
+   _goals_: tracks the no. of goals scored by each player throughout a season

The full data structure for the __CHAMPGAFFER__ database can be found in [schema.sql][]. 

_R A N D O M I S E R . P Y_
---------------------------

__CHAMPGAFFER__ uses various methods from _Python_'s [random][] module to randomise player and club attributes, namely _randint, choices, uniform and shuffle_. This randomiser magic mainly takes place in [randomiser.py][]. 

Each player's skill attributes are as follows, stored in `champgaffer.db`'s _player\_attr_ table, and are unique to each user/manager:

+   Speed
+   Strength
+   Technique
+   Potential
+   Handsomeness
+   Ovr  
+   Age
+   Value

_Speed, strength, technique, potential and handsomeness_ are randomised with `random.choices`, weighted using the ratings of each player's starter club.

The _age_ attribute also uses `random.choices`, but is weighted separately, whilst _ovr_ is calculated using `statistics.mean`.

_Value_ (transfer cost) is computed using a mixture of key player attributes fed into weighted probabilities via `random.choices`, weighted using `random.uniform` for an extra layer of randomness, added to an inital `random.randint` integer. Additional value is added to players whose _potential_ is greater than 17, and whose _handsomeness_ is greater than 17 or whose _handsomeness_ is 2 points greater than their _ovr_ rating:

```python
if potential > 17:
    value += uniform(value * 0.1, value * 0.2)
if handsomeness > 17 or handsomeness > ovr + 2:
    value += uniform(value * 0.2, value * 0.4)
```

Along with the dynamic elements in the _player\_attr_ table, `champgaffer.db` is also seeded with some initial player data, stored in its _players_ table. Firstly, _nationality_ is determined from a weighted dictionary list of nations via `random.choices`. Each dictionary consists of a nationality, a nation code and the file name for a .svg file of the nation's flag, as follows:

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

```python
def gotNews(user, news_id=0, pl_id=0)
```
. . .
```python
def getStory(user, news_id=0, pl_id=0)
```

_N E W S . P Y_
---------------

[news.py][] handles the generation of 22 dynamic news items formatted as emails that appear in a user's Windows '98 inspired 'Me-mail inbox'. The news items keep the user up to date with key game events including transfer offers, budgets, board expectations/confidence, league winners/runner-ups and relegations. These key news items are mixed with more humorous anecdotes regarding the club Chairman (Glenn), his secretary (Morag), the Head Coach (Dave), and players in the user's squad.

[news.py][]'s `getStory` function returns a dictionary with 7 key value pairs.

+   Mail_id
    - which mail item is to be returned
    - entered in `getStory` argument, or randomly generated
+   Sender
    - determined by _mail\_id_
    - changes dependent on _player\_id_, _mail\_id_ and _club\_id_
+   Subject
    - determined by _mail\_id_
    - changes dependent on _player\_id_, _mail\_id_ and _club\_id_
+   Body
    - determined by _mail\_id_
    - changes dependent on _player\_id_, _mail\_id_ and _club\_id_
+   Player_id
    - which player (if any) the news story relates to
    - entered in `getStory` argument, or randomly generated
+   Club_id
    - which club (if any) the news story relates to
    - entered in `getStory` argument, or randomly generated
+   Offer
    - the sum offered if the _mail\_id_ refers to a transfer offer
    - calculated using the [randomiser.py][] `playerValue` function and `random.uniform`

_A P P . P Y_
-------------

[app.py][] pulls the whole shebang together taking care of the routing, template rendering and the majority of the database queries, insertions and updates. It is well commented, and its workings are referenced in the remainder of this document where related to specific pages.


_H T M L ,  C S S  &  L A Y O U T_
-----------------------

The _HTML_ for the project is stored in the _/templates_ folder. Excluding the Teletext-inspired match simulation pages, each __CHAMPGAFFER__ page uses [Flask][] to extend `layout.html`. The head of `layout.html` contains links to global components of the app: 

+   The `main.css` stylesheet, compiled using [less][] with imports of:
    - [Bootstrap][]'s _CSS_
    - [98.css][]: for Windows '98 styling
    - `styles.css`: _CSS_ fine tuning
+   [jQuery][], [popper.js][] and [Bootstrap]'s _JavaScript_
+   [favicon.io][] favicons
+   [font awesome][] icons

`layout.html` also handles the global [Bootstrap][] navigation bar, positioning of [flash messages][] and acknowledgements in the footer. Here also lives the simple loading page, which appends an animated loader icon to a pre-loaded page and removes it once all elements have loaded. A `setTimeout()` fallback is included in the event of a page item failing to load after 5 seconds:

```javascript
$(window).on('load', function(){
    removeLoader(); //wait for page load
});
window.setTimeout(removeLoader, 5000); // fallback if some content fails to load
```

Layout and content alignment for all non-Teletext pages is handled by _Bootstrap_'s [grid system][], ensuring responsiveness and flexibilty in the page layouts.

All _CSS_ and image files can be found in the _/static_ folder. The majority of the application's _JavaScript_ is page specific and can therefore be located in the body of the relevant page's _HTML_. Additional _JavaScript_ files are stored in _/static/js_.

_I N D E X  /  C L U B  P A G E S_
----------------------------------

`index.html` acts as an 'office' for the manager - using Flask-injected _HTML_ to display manager 'emails', along with squad details, star players, upcoming club fixtures, remaining budget and board confidence.

The Windows '98 inspired email and fixture list page elements are adapted from [98.css][]. The fixture window displays the users upcoming fixtures, while the email window provides the user with access to their 10 most recent news items. To give the email UI an authentic flavour, the body of an email is viewable via a customised _Bootstrap_ [modal][]. New emails display in bold with an 'unread' icon, and the content of the news item is passed into the modal on click. Unread items are determined by a boolean in the _read_ column of the `champgaffer.db` _news_ table, which defaults to 0 (false) when a news item is generated.

Emails are dynamically marked as 'read' without reloading the page using a form passed to the `"/read"` route in an [Ajax][] request - sent on opening the news modal. If the request is successful, the `champgaffer.db` _news_ table's _read_ column is set to 1, the unread icon is switched out and font weight set to normal:

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

Player cards are styled loosely on 80s/90s Panini [football stickers][], using [DiceBear][] generated avatars, nation flags, team colours and player statistics pulled from the `champgaffer.db` _player\_attr_ table. The manager card and star player cards are included in the flow of the `index.html` and `club.html` pages. Player cards for squad players can also be viewed as _Bootstrap_ [modal][] windows accessed through clickable rows in the squad list tables.

`club.html` is a stripped back version of `index.html`, which provides dynamic information for each club in the user's universe. Emails and fixtures are ommitted, but club/manager stats, star players and squad lists (including player card modals) are all viewable.

The dynamic club pages are accessible through Javascript constructed URLs when clicking a club's name in the _standings_, _stats_ and _matchday_ pages - or in a player modal:

```javascript
var club_link = club['club_name'].replace(" ", "_")
```

The club routes are handled in [app.py][]'s `profile` function, querying `champgaffer.db` for the relevant club info:

```python
@app.route("/<club_name>")
@login_required
def profile(club_name):
    """Display club info"""

    # identify club
    session['clubInfo'] = db.execute("SELECT * FROM clubs JOIN club_attr ON clubs.club_id = club_attr.club_id WHERE (club_name = ? AND club_attr.manager_id = ?) AND clubs.club_id < 20;",
                      club_name.replace("_", " "), session['id'])
```



[Championship Manager]: https://en.wikipedia.org/wiki/Championship_Manager      "Championship Manager Wikipedia page"
[Bootstrap]: https://getbootstrap.com/      "Bootstrap site"
[Teletext]: https://en.wikipedia.org/wiki/Teletext      "Teletext Wikipedia page"
[SQLite]: https://www.sqlite.org/index.html     "SQLite site"
[form-control]: https://getbootstrap.com/docs/4.0/components/forms/#form-controls       "Bootstrap form-control docs"
[flash messages]: https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/     "Flask message flashing docs"
[generate_password_hash]: https://werkzeug.palletsprojects.com/en/1.0.x/utils/      "Werkzeug utilities documentation"
[Flask-Session]: https://pypi.org/project/Flask-Session/    "Flask-Session docs"
[news.py]: news.py        "This file handles the generation of news emails"
[schema.sql]: schema.sql       "Champgaffer data tables"
[random]: https://docs.python.org/3/library/random.html     "Python random docs"
[Faker]: https://faker.readthedocs.io/en/master/        "Python Faker docs"
[randomiser.py]: randomiser.py     "This file handles player/fixture randomising"
[round robin]: https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm        "Round robin scheduling on Wikipedia"
[generator.py]: generator.py    "This file handles the generation of various game attributes unique to each user"
[news.py]: news.py      "This file handles the generation of news items unique to each user"
[app.py]: app.py        "Main application file for Champgaffer"
[Flask]: https://flask.palletsprojects.com/en/1.1.x/    "Flask docs"
[less]: http://lesscss.org/     "Less"
[98.css]: https://jdan.github.io/98.css/    "Adapted for the 'Windowfied' elements of the app"
[jQuery]: https://jquery.com/       "jQuery site"
[popper.js]: https://popper.js.org/     "popper.js (tooltip and popover positioning) site"
[grid system]: https://getbootstrap.com/docs/4.5/layout/grid/       "Bootstrap grid system docs"
[modal]: https://getbootstrap.com/docs/4.5/components/modal/        "Bootstrap modal docs"
[Ajax]: https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX     "MDN Ajax docs"
[football stickers]: https://www.theguardian.com/sport/gallery/2013/may/15/beautiful-games-old-panini-stickers-gallery        "Guardian old school Panini"
[DiceBear]: https://avatars.dicebear.com/       "DiceBear avatars docs"

