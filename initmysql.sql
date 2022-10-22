USE mysql;
CREATE USER MY_ROOT_USER@$MYSQL_IP IDENTIFIED BY $MYSQL_ROOT_PASSWORD;
GRANT ALL PRIVILEGES ON *.* TO MY_ROOT_USER@$MYSQL_IP;
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS bot;
USE bot
CREATE TABLE IF NOT EXISTS 'users' (id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    user_id_bot VARCHAR(255),
                                    search_phrase TEXT NOT NULL DEFAULT '',
                                    link_view TEXT NOT NULL DEFAULT '',
                                    link_download TEXT NOT NULL DEFAULT ''
                                    );
INSERT INTO users(user_id_bot,search_phrase,link_view,link_download)
VALUES ('999999','strangeshithappened','https://polonsky.net','https://aws.com')