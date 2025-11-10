from .db import get_conn
from . import list as list_mod


def add_item(list_id: int, name: str, target_quantity: int = 1):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO items (list_id, name, target_quantity, version) VALUES (?, ?, ?, 0)',
        (list_id, name, target_quantity),
    )
    conn.commit()
    item_id = cur.lastrowid
    
    # Increment list version
    list_mod._increment_list_version(list_id, conn)
    
    conn.close()
    return item_id


def remove_item(item_id: int):
    conn = get_conn()
    cur = conn.cursor()
    
    # Get list_id before deletion
    cur.execute('SELECT list_id FROM items WHERE id = ?', (item_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return
    
    list_id = row['list_id']
    
    cur.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    
    # Increment list version
    list_mod._increment_list_version(list_id, conn)
    
    conn.close()


def list_items(list_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, checked, target_quantity, acquired_quantity, version FROM items WHERE list_id = ? ORDER BY id', (list_id,))
    items = [dict(r) for r in cur.fetchall()]
    conn.close()
    return items


def toggle_checked(item_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT checked, list_id FROM items WHERE id = ?', (item_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    
    new = 0 if row['checked'] else 1
    list_id = row['list_id']
    
    cur.execute('UPDATE items SET checked = ?, version = version + 1 WHERE id = ?', (new, item_id))
    conn.commit()
    
    # Increment list version
    list_mod._increment_list_version(list_id, conn)
    
    conn.close()
    return True


def set_acquired(item_id: int, acquired: int):
    conn = get_conn()
    cur = conn.cursor()
    
    # Get list_id
    cur.execute('SELECT list_id FROM items WHERE id = ?', (item_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return
    
    list_id = row['list_id']
    
    cur.execute('UPDATE items SET acquired_quantity = ?, version = version + 1 WHERE id = ?', (acquired, item_id))
    conn.commit()
    
    # Increment list version
    list_mod._increment_list_version(list_id, conn)
    
    conn.close()
