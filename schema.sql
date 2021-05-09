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

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    project TEXT,
    made_at TIMESTAMP,
    done BOOLEAN
);

CREATE TABLE project_members (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects,
    user_id INTEGER REFERENCES users
);

CREATE TABLE project_tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects,
    creator_id INTEGER REFERENCES users,
    task TEXT,
    priority INTEGER,
    made_at TIMESTAMP,
    done BOOLEAN
);

CREATE TABLE project_task_comments (
    id SERIAL PRIMARY KEY,
    project_task_id INTEGER REFERENCES project_tasks,
    creator_id INTEGER REFERENCES users,
    comment TEXT,
    made_at TIMESTAMP,
    visible BOOLEAN,
);
