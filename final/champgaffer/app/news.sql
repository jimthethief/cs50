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