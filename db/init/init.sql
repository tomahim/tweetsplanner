CREATE TABLE players ( firstname VARCHAR(100) NOT NULL, lastname VARCHAR(100) NOT NULL );

INSERT INTO players VALUES ('james', 'lebron');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(32) NOT NULL,
    twitter_id VARCHAR(32) NOT NULL,
    oauth_token VARCHAR(255) NOT NULL,
    oauth_secret VARCHAR(255) NOT NULL
);

CREATE TABLE jwt_blacklist (
    id SERIAL PRIMARY KEY,
    token TEXT NOT NULL
);