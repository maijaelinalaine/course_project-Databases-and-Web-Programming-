import db
from datetime import datetime
def add_event(title, event_time, description, event_type, user_id):
    try:
        if "T" in event_time:
            event_time = datetime.strptime(event_time, "%Y-%m-%dT%H:%M")
        else:
            event_time = datetime.strptime(event_time, "%Y-%m-%d")
        
        event_time_formatted = event_time.strftime("%Y-%m-%d %H:%M:%S")
        
        sql = """INSERT INTO events (title, event_time, description, event_type, user_id)
                VALUES (?, ?, ?, ?, ?)"""
        
        db.execute(sql, [title, event_time_formatted, description, event_type, user_id])

        return db.last_insert_id()
        
    except ValueError as e:
        print(f"Date format error: {e}")
        raise ValueError(f"Virheellinen päivämäärän muoto: {event_time}")
    except Exception as e:
        print(f"Database error in add_event: {e}")
        raise

def get_events():
    sql = """SELECT id, title FROM events ORDER BY id DESC"""

    return db.query(sql)

def get_event(event_id):
    sql = """SELECT e.title,
                    e.event_time,
                    e.description,
                    e.event_type,
                    u.id AS user_id,
                    u.username
            FROM events e, users u
            JOIN users ON e.user_id = u.id
            WHERE e.id = ?"""
    result = db.query(sql, [event_id])

    if result:
        return result[0]
    else:
        return None

def edit_event(event_id, description):
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
    