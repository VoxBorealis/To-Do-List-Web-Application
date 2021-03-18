CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    task TEXT,
    made_at TIMESTAMP,
    done BOOLEAN
);