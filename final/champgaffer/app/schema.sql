CREATE TABLE clubs (club_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    club_name TEXT NOT NULL, 
                    primary_colour TEXT NOT NULL, 
                    secondary_colour TEXT NOT NULL, 
                    manager TEXT NOT NULL, 
                    desc TEXT NOT NULL, 
                    capacity INTEGER, 
                    rival INTEGER);

CREATE UNIQUE INDEX club_name ON clubs(club_name);

CREATE TABLE managers (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                       username TEXT NOT NULL, 
                       hash TEXT NOT NULL, 
                       club_id INTEGER NOT NULL, 
                       name TEXT NOT NULL, 
                       club_name TEXT NOT NULL DEFAULT "Noname Athletic",
                       age INTEGER NOT NULL DEFAULT 40, 
                       board_confidence INTEGER NOT NULL DEFAULT 80, 
                       budget NUMERIC NOT NULL DEFAULT 15.00, 
                       matchday INTEGER NOT NULL DEFAULT 1, 
                       season INTEGER NOT NULL DEFAULT 2020,
                       current_season INTEGER DEFAULT 2020,  
                       FOREIGN KEY (club_id) REFERENCES clubs(club_id));
                       
CREATE UNIQUE INDEX username on managers(username);
                       
CREATE TABLE players (player_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                      starter_club TEXT NOT NULL,
                      name TEXT NOT NULL, 
                      nationality TEXT NOT NULL, 
                      flag TEXT NOT NULL, 
                      pos TEXT NOT NULL,
                      FOREIGN KEY (starter_club) REFERENCES clubs(club_name));

CREATE UNIQUE INDEX player_id on players(player_id);

CREATE TABLE club_attr (manager_id INTEGER NOT NULL,
                        club_id INTEGER NOT NULL,
                        rank INTEGER NOT NULL,
                        ovr INTEGER NOT NULL,
                        formation TEXT NOT NULL DEFAULT "4-4-2",
                        attendance REAL NOT NULL, 
                        pld INTEGER NOT NULL DEFAULT 0;
                        gs INTEGER NOT NULL DEFAULT 0;
                        ga INTEGER NOT NULL DEFAULT 0;
                        pts INTEGER NOT NULL DEFAULT 0;
                        pos INTEGER NOT NULL DEFAULT 0;
                        pos_track INTEGER NOT NULL DEFAULT 0;
                        FOREIGN KEY (manager_id) REFERENCES managers(id), 
                        FOREIGN KEY (club_id) REFERENCES clubs(club_id));

CREATE TABLE player_attr (manager_id INTEGER NOT NULL, 
                          player_id INTEGER NOT NULL, 
                          club_id INTEGER NOT NULL, 
                          age INTEGER NOT NULL,
                          speed NUMERIC NOT NULL, 
                          strength NUMERIC NOT NULL, 
                          technique NUMERIC NOT NULL, 
                          potential NUMERIC NOT NULL, 
                          handsomeness NUMERIC NOT NULL, 
                          ovr NUMERIC NOT NULL, 
                          value NUMERIC NOT NULL,
                          FOREIGN KEY (manager_id) REFERENCES managers(id), 
                          FOREIGN KEY (player_id) REFERENCES players(player_id),
                          FOREIGN KEY (club_id) REFERENCES clubs(club_id));

CREATE TABLE fixtures (fixture_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       manager_id INTEGER NOT NULL,
                       season INTEGER NOT NULL, 
                       week INTEGER NOT NULL,
                       home TEXT NOT NULL,
                       away TEXT NOT NULL,
                       played BOOLEAN NOT NULL CHECK (played IN (0,1)) DEFAULT 0,
                       FOREIGN KEY(manager_id) REFERENCES managers(id));

CREATE TABLE goals (goal_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    manager_id INTEGER NOT NULL,
                    player_id INTEGER NOT NULL,
                    week INTEGER NOT NULL,
                    season INTEGER NOT NULL,
                    FOREIGN KEY (manager_id) REFERENCES managers(id),
                    FOREIGN KEY (player_id) REFERENCES players(player_id));

CREATE TABLE news (news_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   manager_id INTEGER NOT NULL,
                   player_id INTEGER DEFAULT 0,
                   club_id INTEGER DEFAULT 0,
                   message_id INTEGER NOT NULL,
                   sender TEXT NOT NULL,
                   subject TEXT NOT NULL,
                   body TEXT NOT NULL,
                   read BOOLEAN NOT NULL CHECK (read IN (0,1)) DEFAULT 0,
                   FOREIGN KEY (manager_id) REFERENCES managers(id));