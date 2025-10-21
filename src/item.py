from .db import get_conn


def add_item(list_id: int, name: str, target_quantity: int = 1):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO items (list_id, name, target_quantity) VALUES (?, ?, ?)',
        (list_id, name, target_quantity),
    )
    conn.commit()
    item_id = cur.lastrowid
    conn.close()
    return item_id


def remove_item(item_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()


def list_items(list_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, checked, target_quantity, acquired_quantity FROM items WHERE list_id = ?', (list_id,))
    items = [dict(r) for r in cur.fetchall()]
    conn.close()
    return items


def toggle_checked(item_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT checked FROM items WHERE id = ?', (item_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    new = 0 if row['checked'] else 1
    cur.execute('UPDATE items SET checked = ? WHERE id = ?', (new, item_id))
    conn.commit()
    conn.close()
    return True


def set_acquired(item_id: int, acquired: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('UPDATE items SET acquired_quantity = ? WHERE id = ?', (acquired, item_id))
    conn.commit()
    conn.close()
