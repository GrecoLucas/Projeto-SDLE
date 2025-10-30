CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE shopping_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE list_shares (
    list_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (list_id, user_id),
    FOREIGN KEY (list_id) REFERENCES shopping_lists(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    checked BOOLEAN DEFAULT 0,
    target_quantity INTEGER DEFAULT 1,
    acquired_quantity INTEGER DEFAULT 0,
    FOREIGN KEY (list_id) REFERENCES shopping_lists(id)
);
