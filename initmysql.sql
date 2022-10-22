CREATE DATABASE IF NOT EXISTS bot;
GRANT ALL PRIVILEGES ON bot.* TO 'ilya'@'192.168.20.180';
USE bot
CREATE TABLE IF NOT EXISTS 'users' (id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    user_id_bot VARCHAR(255),
                                    search_phrase TEXT NOT NULL DEFAULT '',
                                    link_view TEXT NOT NULL DEFAULT '',
                                    link_download TEXT NOT NULL DEFAULT ''
                                    );
INSERT INTO users(user_id_bot,search_phrase,link_view,link_download)
VALUES ('999999','strangeshithappened','https://polonsky.net','https://aws.com')