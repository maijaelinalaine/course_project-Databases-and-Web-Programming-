import db

def add_event(title, description, type, user_id):
    sql = """INSERT INTO events (title, description, type, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, type, user_id])

def get_events():
    sql = """SELECT id, title FROM items ORDER BY id DESC"""
    return db.query(sql)

def get_event(event_id):
    sql = """SELECT events.title,
                    events.description,
                    events.type,
                    users.username
            FROM events, users
            WHERE events.user_id = user_id
            AND events.id = ?"""
    return db.query(sql, [event_id])[0]