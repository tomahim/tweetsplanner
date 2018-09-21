CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(32) NOT NULL,
    twitter_id VARCHAR(32) NOT NULL,
    oauth_token VARCHAR(255) NOT NULL,
    oauth_secret VARCHAR(255) NOT NULL
);

CREATE TYPE tweet_status AS ENUM ('DRAFT', 'PLANNED', 'SENDED');
CREATE TABLE tweets (
    id SERIAL PRIMARY KEY,
    user_id integer REFERENCES users (id),
    text TEXT,
    send_date timestamp with time zone,
    status tweet_status NOT NULL
);

CREATE TABLE jwt_blacklist (
    id SERIAL PRIMARY KEY,
    token TEXT NOT NULL
);