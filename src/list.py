from .db import get_conn


def _increment_list_version(list_id: int, conn=None):
    """Increment the version counter of a shopping list."""
    close_conn = False
    if conn is None:
        conn = get_conn()
        close_conn = True
    
    cur = conn.cursor()
    cur.execute(
        'UPDATE shopping_lists SET version = version + 1, last_modified = CURRENT_TIMESTAMP WHERE id = ?',
        (list_id,)
    )
    conn.commit()
    
    if close_conn:
        conn.close()


def create_list(name: str):
    """Create a shopping list (no owner). Lists are shared with all users by default."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO shopping_lists (name, version) VALUES (?, 0)', (name,))
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
    cur.execute('SELECT id, name, version, last_modified FROM shopping_lists ORDER BY last_modified DESC')
    rows = [dict(r) for r in cur.fetchall()]
    # keep owner_id key for compatibility with UI, set to None
    for r in rows:
        r['owner_id'] = None
    conn.close()
    return {'owned': [], 'shared': rows}


