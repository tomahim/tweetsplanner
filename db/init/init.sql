CREATE TABLE players ( firstname VARCHAR(100) NOT NULL, lastname VARCHAR(100) NOT NULL );

INSERT INTO players VALUES ('james', 'lebron');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(32) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- password: toto
INSERT INTO users (username, password) VALUES ('tom', 'pbkdf2:sha256:50000$N2HQR6W1$92c0e957477de2ef4f953ae99ab3b46aea8f712b3f56f8ca7a988b122139722a');
