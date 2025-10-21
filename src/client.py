from .db import get_conn


def get_or_create_user(name: str):
	conn = get_conn()
	cur = conn.cursor()
	cur.execute('SELECT id, name FROM users WHERE name = ?', (name,))
	row = cur.fetchone()
	if row:
		user = dict(row)
	else:
		cur.execute('INSERT INTO users (name) VALUES (?)', (name,))
		conn.commit()
		user_id = cur.lastrowid
		user = {'id': user_id, 'name': name}
	conn.close()
	return user


def get_user_by_id(user_id: int):
	conn = get_conn()
	cur = conn.cursor()
	cur.execute('SELECT id, name FROM users WHERE id = ?', (user_id,))
	row = cur.fetchone()
	conn.close()
	return dict(row) if row else None


