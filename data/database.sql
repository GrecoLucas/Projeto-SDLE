CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE shopping_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
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
