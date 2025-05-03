import db
from datetime import datetime

def get_event_types():
    sql = """SELECT title
            FROM event_types
        """
    
    result = db.query(sql)

    event_types = []
    for title in result:
        event_types.append((title["title"]))
    
    return event_types

def add_event(title, event_time, description, event_type, user_id):
    try:
        if "T" in event_time:
            event_time = datetime.strptime(event_time, "%Y-%m-%dT%H:%M")
        else:
            event_time = datetime.strptime(event_time, "%Y-%m-%d")
        
        event_time_formatted = event_time.strftime("%Y-%m-%d %H:%M")
        
        sql = """INSERT INTO events 
            (title, event_time, description, event_type, user_id)
                VALUES (?, ?, ?, ?, ?)"""
        
        db.execute(sql, [title, event_time_formatted, description, event_type, user_id])

        event_id = db.last_insert_id()

        return event_id
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def signup(event_id, user_id):
    sql = """INSERT INTO signups (event_id, user_id, signup_time)
            VALUES (?, ?, ?)"""
        
    db.execute(sql, [event_id, user_id, datetime.now().strftime("%Y-%m-%d %H:%M")])

def get_signups(event_id):
    sql = """SELECT u.id, u.username, s.signup_time
            FROM users u, signups s
            WHERE s.event_id = ?
            AND s.user_id = u.id
            ORDER BY s.signup_time ASC"""
    
    return db.query(sql, [event_id])

def get_events():
    sql = """SELECT id, title, event_time
            FROM events 
            ORDER BY event_time ASC"""
    
    return db.query(sql)

def get_event(event_id):
    sql = """SELECT e.id,
                    e.title,
                    e.event_time,
                    e.description,
                    e.event_type,
                    u.id AS user_id,
                    u.username
            FROM events e, users u
            JOIN users ON e.user_id = u.id
            WHERE e.id = ?"""
    result = db.query(sql, [event_id])

    return result[0] if result else None
   
def update_event(event_id, title, event_time, description, event_type):
    sql = "UPDATE events SET title = ?, description = ?, event_time = ?, event_type = ? WHERE id = ?"
    db.execute(sql, [title, description, event_time, event_type, event_id])

def remove_event(event_id):
    sql = "DELETE FROM events WHERE id = ?"
    db.execute(sql, [event_id])

def search(query):
    sql = """SELECT id, event_time, title, event_type
            FROM events e
            WHERE event_type LIKE ? OR title LIKE ?
            ORDER BY event_time ASC"""
    like = "%" + query + "%"
    
    return db.query(sql, [like, like])
    