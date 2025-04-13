import db

def add_event(title, description, event_type, user_id):
    sql = """INSERT INTO events (title, description, event_type, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, event_type, user_id])

def get_events():
    sql = """SELECT id, title FROM events ORDER BY id DESC"""
    return db.query(sql)

def get_event(event_id):
    sql = """SELECT events.title,
                    events.description,
                    events.event_type,
                    users.id user_id,
                    users.username
            FROM events, users
            WHERE events.user_id = user_id
            AND events.id = ?"""
    return db.query(sql, [event_id])[0]

def update_event(event_id, description):
    sql = "UPDATE events SET description = ? WHERE id = ?"
    db.execute(sql, [description, event_id])

def remove_event(event_id):
    sql = "DELETE FROM events WHERE id = ?"
    db.execute(sql, [event_id])

def search(query):
    sql = """SELECT e.id event_id,
                    e.title,
                    e.description,
                    e.event_type,
                    u.username
            FROM events e, users u
            WHERE e.user_id = u.id
            AND (e.event_type LIKE ?)
            ORDER BY e.id DESC"""
    return db.query(sql, ["%" + query + "%"])
    