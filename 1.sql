CREATE TABLE IF NOT EXISTS 'users' (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id_bot VARCHAR(255)
	search_phrase TEXT
	link_view TEXT
	link_download TEXT
);
INSERT INTO users(user_id_bot,search_phrase,link_view,link_download) VALUES ('999999','strangeshithappened','https://polonsky.net','https://aws.com')