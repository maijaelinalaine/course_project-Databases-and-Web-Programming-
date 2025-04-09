import db

def add_items(title, description, type, user_id):
    sql = """INSERT INTO events (title, description, type, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, type, user_id])
 