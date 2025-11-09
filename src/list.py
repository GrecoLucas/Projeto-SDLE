from .db import get_conn


def create_list(name: str):
    """Create a shopping list (no owner). Lists are shared with all users by default."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO shopping_lists (name) VALUES (?)', (name,))
    conn.commit()
    list_id = cur.lastrowid
    conn.close()
    return list_id


def remove_list(list_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM items WHERE list_id = ?', (list_id,))
    cur.execute('DELETE FROM shopping_lists WHERE id = ?', (list_id,))
    conn.commit()
    conn.close()


def get_lists_for_user(user_id: int):
    """Return all lists as 'shared' because every list is shared with all users."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM shopping_lists')
    rows = [dict(r) for r in cur.fetchall()]
    # keep owner_id key for compatibility with UI, set to None
    for r in rows:
        r['owner_id'] = None
    conn.close()
    return {'owned': [], 'shared': rows}


