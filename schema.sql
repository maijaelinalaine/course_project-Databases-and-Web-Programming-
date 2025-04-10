CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    event_type TEXT,
    user_id INTEGER REFERENCES users
);