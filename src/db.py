import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "db.sqlite"
SCHEMA_SQL = Path(__file__).resolve().parents[1] / "data" / "database.sql"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'database.sql'


def init_db(force: bool = False):
    """Create the sqlite database and initialize schema from data/database.sql.

    If force is True, existing DB will be replaced.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists() and not force:
        return
    if DB_PATH.exists() and force:
        DB_PATH.unlink()

    if not SCHEMA_SQL.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_SQL}")

    conn = sqlite3.connect(DB_PATH)
    with SCHEMA_SQL.open("r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)
    conn.commit()
    conn.close()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")
    conn = get_conn()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        sql = f.read()
    conn.executescript(sql)
    conn.commit()
    conn.close()

def get_all_users():
    """Return a list of all users in the database."""
    conn = get_conn()
    cursor = conn.execute("SELECT name FROM users")
    users = [row["name"] for row in cursor.fetchall()]
    conn.close()
    return users

def destroy_db():
    """Delete the existing database file."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    return not DB_PATH.exists()