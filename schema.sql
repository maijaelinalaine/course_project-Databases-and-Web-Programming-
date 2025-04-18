CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_time DATETIME,
    title TEXT,
    description TEXT,
    event_type TEXT,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE event_types (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE signups (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    user_id INTEGER REFERENCES users(id),
    signup_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, user_id)
);