CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    task TEXT,
    priority INTEGER,
    made_at TIMESTAMP,
    done BOOLEAN
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    task_id INTEGER REFERENCES tasks,
    comment TEXT,
    visible BOOLEAN
);