from werkzeug.security import check_password_hash, generate_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id

    return None

def get_user(user_id):
    sql = """SELECT id, username, registered_at
            FROM users
            WHERE id = ?"""
    result = db.query(sql, [user_id])

    return result[0] if result else None

def get_events(user_id):
    sql = """SELECT e.id, e.title, e.event_time, e.description, e.event_type
            FROM events e
            WHERE e.user_id = ? 
            ORDER BY e.event_time ASC"""
    
    result = db.query(sql, [user_id])

    return result if result else None

def get_signups(user_id):
    sql = """SELECT e.id, e.title, e.event_time, e.description, e.event_type
            FROM events e
            JOIN signups s ON e.id = s.event_id
            WHERE s.user_id = ? 
            ORDER BY e.event_time ASC"""
    
    result = db.query(sql, [user_id])

    return result if result else None