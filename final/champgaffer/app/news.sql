CREATE TABLE news (news_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   manager_id INTEGER NOT NULL,
                   player_id INTEGER DEFAULT NULL,
                   club_id INTEGER DEFAULT NULL,
                   message_id INTEGER NOT NULL,
                   sender TEXT NOT NULL,
                   subject TEXT NOT NULL,
                   body TEXT NOT NULL,
                   FOREIGN KEY (manager_id) REFERENCES managers(id));