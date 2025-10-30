from .db import get_conn


def create_list(owner_id: int, name: str):
    """Create a shopping list with an owner and a name."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO shopping_lists (owner_id, name) VALUES (?, ?)', (owner_id, name))
    conn.commit()
    list_id = cur.lastrowid
    conn.close()
    return list_id


def remove_list(list_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM items WHERE list_id = ?', (list_id,))
    cur.execute('DELETE FROM list_shares WHERE list_id = ?', (list_id,))
    cur.execute('DELETE FROM shopping_lists WHERE id = ?', (list_id,))
    conn.commit()
    conn.close()


def get_lists_for_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    # lists owned (include name)
    cur.execute('SELECT id, owner_id, name FROM shopping_lists WHERE owner_id = ?', (user_id,))
    owned = [dict(r) for r in cur.fetchall()]
    # lists shared (include name)
    cur.execute('''
        SELECT sl.id, sl.owner_id, sl.name FROM shopping_lists sl
        JOIN list_shares ls ON ls.list_id = sl.id
        WHERE ls.user_id = ?
    ''', (user_id,))
    shared = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {'owned': owned, 'shared': shared}


def share_list(list_id: int, user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO list_shares (list_id, user_id) VALUES (?, ?)', (list_id, user_id))
        conn.commit()
    except Exception:
        # ignore duplicate or foreign key errors for simplicity
        pass
    finally:
        conn.close()
